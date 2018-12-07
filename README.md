# slurm-cpu-bind-mask-generator
Generates bit masks for Slurm's cpu_bind:mask_cpu 

If you ever needed to do a low-level cpu binding on SLURM, you know this page: [https://slurm.schedmd.com/mc_support.html#srun_lowlevelmc]

Example: if you have a 48-core compute node, and you want to pin 8 MPI processes with 6 OpenMPI threads each in your machine, you can just say: --cpus-per-task=6

And this will be your pinning:

```
CPU:
1                                              48
******------------------------------------------
------******------------------------------------
------------******------------------------------
------------------******------------------------
------------------------******------------------
------------------------------******------------
------------------------------------******------
------------------------------------------******
```

Slurm lets you do manual pinning, with the options --cpu_bind=map_cpu, and --cpi_bind=mask_cpu. This project is for the second. For example, 

```
srun -n 2 --cpu_bind=mask_cpu:0x3,0xC
```

spawns two tasks pinned to cores 0 and 1 (0x3 = 3 = 20 + 21) and cores 2 and 3 (0xC = 11 = 22 + 23), respectively.

To write those pinnings by hand, in a big machine, is a PITA. So I wrote this little script. 

# Usage:

```
python3 maskgenerator.py <cores> <processes> [rank or -r]
```

- Where ```cores``` are the number of SMT cores of your compute node, 
- ```processes``` are the number of MPI processes this node will run, 
- and [rank] is optionally the rank number to which a mask should be generated. If not, it generates a mask for all ranks. 

The optional [-r] setting creates a aleatory distribution, so processes are pinned randomly. Useful to check if processes really benefit from advanced pinning. 

# Using it on [JUBE, the JUelich Benchmark Environment](http://www.fz-juelich.de/ias/jsc/EN/Expertise/Support/Software/JUBE/JUBE2/jube-download_node.html)
```
<parameter name="cpu_bind_mask" separator=";" mode="shell">module load Python/3.6.6; python3 maskgenerator.py 48 ${taskspernode}</parameter>
<parameter name="args_starter" separator=";">--cpu_bind=verbose,mask_cpu:$cpu_bind_mask</parameter>
```
