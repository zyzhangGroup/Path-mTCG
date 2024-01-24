<picture>
 <source media="(prefers-color-scheme: dark)" srcset="YOUR-DARKMODE-IMAGE">
 <source media="(prefers-color-scheme: light)" srcset="YOUR-LIGHTMODE-IMAGE">
 <img alt="YOUR-ALT-TEXT" src="YOUR-DEFAULT-IMAGE">
</picture>

# Path-mTCG
The assembly order of its protein subunits is functionally very important. In this work, we developed a computational tool for predicting the disassembly and assembly order of protein complexes using coarse-grained simulations at multiple temperatures. 

## Installation
1. Download CafeMol 3.2.1 version in https://www.cafemol.org/
2.  Change the CafeMol installation path (`path_para` and `path_aicg`)in the input file(`example/Input/*.inp`) based on your installation directory
3. Prepare the PDB file(eg: `arp23.pdb`) and place it at the `example/Input` directory
4. Set the minimum temperature (`T_min`), the maximum temperature (`T_max`), the number ofsubunits (`n`), the protein name (`Pro_name`) and the hostlists (`hostlists`) in the `submit_run.py` file. The `Pro_name` must be the same as the pdb file name(eg: `Pro_name="arp23"`)
5. Run the execution file `submit_run.py` and set the output file name(eg: `arp23.out`)

## Usage
Run ```nohup python submit_run.py > *.out &```

## Author
Yunxiao Lu & Zhiyong Zhang


