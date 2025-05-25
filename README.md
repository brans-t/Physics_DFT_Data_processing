# Physics_DFT_Data_processing
---
## Subprogram1: PLOT
---

## Subprogram2: Band Calculations Batch
---

### Step 1: Prepare Input Files
---

> 1. **Prepare the chemical formulas and POTCAR pseudopotential files**:
>
> For example, if we need to prepare the following chemical formulas for `POTCAR`, we can list all the chemical formulas to be calculated in an `atom` file:
>
> ```
> "atom" file:
> -----------------------------------------------------------------------------------
> Cr2OSTe
> Cr2OSeS
> Cr2OSeTe
> Mo2SSeS
> Mo2STeS
> -----------------------------------------------------------------------------------
> ```
>
> Next, we need to prepare the required `POTCAR` pseudopotential files for these elements and place them in a folder named `POTCAR`:
>
> ```
> "POTCAR" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─POTCAR
>         POTCAR_Cr
>         POTCAR_Mo
>         POTCAR_O
>         POTCAR_S
>         POTCAR_Se
>         POTCAR_Te
> -----------------------------------------------------------------------------------
> ```
>
> **Note:** The pseudopotential files must be uniformly named as `POTCAR_XXX`.

> 2. **Prepare the files required for structural optimization (`INCAR`, `KPOINTS`, `POSCAR`, `POTCAR`) and the job submission script (`vasp.pbs`)**:
>
> We need to create a folder named `source_file` and place these files inside:
>
> ```
> "source_files" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─source_file
> 	        INCAR
> 	        KPOINTS
> 	        POSCAR
> 	        vasp.pbs
> ---------------------------------------------------------------------------------- 
> ```

> 3. **Prepare the files required for self-consistent field (SCF) calculations (`INCAR`, `KPOINTS`) and the job submission script (`vasp.pbs`)**:
>
> We need to create a folder named `Con_source` and place these files inside:
>
> ```
> "Con_source" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─Con_source
> 	        INCAR
> 	        KPOINTS
> 	        vasp.pbs
> ---------------------------------------------------------------------------------- 
> ```

> 4. **Prepare the files required for band structure calculations (`INCAR`, `KPOINTS`)**:
>
> We need to create a folder named `Band_source` and place these files inside:
>
> ```
> "Band_source" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─Band_source
> 	        INCAR
> 	        KPOINTS
> ---------------------------------------------------------------------------------- 
> ```

**All filenames and folder names must strictly follow the above naming conventions!**

### Step 2: Generate Folder Names and POTCAR Files
---

> 1. **Run the `POTCAR_process.py` script to generate the `Tot_Band` folder**:
>
> The `Tot_Band` folder will have the following structure:
>
> ```
> "Tot_Band" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─ Tot_Band
> 		  ├─Cr_O_Se_S
> 		  |    ├─input
> 		  |        ├─ POTCAR  
> 		  |
> 		  |         
>          ├─F_N_As_Te
>          |    ├─input
> 		  |        ├─ POTCAR 
> 		  |
>          ├─Mo_Se_Te_Se    
>          |    ├─input
> 		  |        ├─ POTCAR
>          .
>          .
>          ....
> -----------------------------------------------------------------------------------
> ```
>
> * This command will automatically create the `Tot_Band` folder and its subfolders named after the chemical formulas (e.g., `XX_XX_XX`). The `POTCAR` file in the `input` subfolder is a combined `POTCAR`.

> 2. **Run the `POSCAR_process.py` script to import the `POSCAR` file into the `input` folder**:
>
> The folder structure will now look like this:
>
> ```
> "Tot_Band" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─ Tot_Band
> 		  ├─Cr_O_Se_S
> 		  |    ├─input
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |         
>          ├─F_N_As_Te
>          |    ├─input
> 		  |        ├─ POTCAR
> 		  |           POSCAR 
> 		  |
>          ├─Mo_Se_Te_Se    
>          |    ├─input
> 		  |        ├─ POTCAR
>          .           POSCAR
>          .
>          ....
> -----------------------------------------------------------------------------------
> ```
>
> * This command will automatically read the `POSCAR` file from the `source_files` folder and replace the element names in lines 6 and 7 with those in the current directory's chemical formula. For example, in the `Cr_O_S_Te` directory, it will change `Xx     Xx    X` to `Cr    O    S    Te`.

> 3. **Run the `element_folder_copier.py` script to import the `INCAR`, `KPOINTS`, and `vasp.pbs` files into the `input` folder**:
>
> The folder structure will now be:
>
> ```
> "Tot_Band" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─ Tot_Band
> 		  ├─Cr_O_Se_S
> 		  |    ├─input
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs
> 		  |         
>          ├─F_N_As_Te
>          |    ├─input
> 		  |        ├─ POTCAR
> 		  |           POSCAR 
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs
> 		  |
>          ├─Mo_Se_Te_Se    
>          |    ├─input
> 		  |        ├─ POTCAR
>          |           POSCAR
>          |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs
>          .
>          ....
> -----------------------------------------------------------------------------------
> ```
>
> **At this point, all the input files required for the calculations have been prepared and placed in the `input` subfolders of the corresponding chemical formulas.**

### Step 3: Perform Structural Optimization Calculations
---

> 1. **Run the `Opt_creat.py` script to automatically create the `opt` folder and place the five input files required for structural optimization inside**:
>
> The folder structure will now look like this:
>
> ```
> "Tot_Band" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─ Tot_Band
> 		  ├─Cr_O_Se_S
> 		  |    ├─input 
> 		  |    |    ├─ POTCAR
> 		  |    |       POSCAR 
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs
> 		  |    ├─opt
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs  
> 		  |         
>          ├─F_N_As_Te
>          |    ├─input
> 		  |    |    ├─ POTCAR
> 		  |    |       POSCAR 
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs
> 		  |    ├─opt
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs 
> 		  |
>          ├─Mo_Se_Te_Se    
>          |    ├─input
> 		  |    |    ├─ POTCAR
>          |    |       POSCAR
>          |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs
> 		  |    ├─opt
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs 
>          .
>          ....
> -----------------------------------------------------------------------------------
> ```

> 2. **Run the `Sub_opt.py` script to automatically submit the `vasp.pbs` job submission script in each `opt` folder**.

### Step 4: Perform Static Self-Consistent Field (SCF) Calculations
---

> 1. **Run the `Con_creat.py` script to automatically create the `con` folder and place the five input files required for SCF calculations inside**:
>
> The program will rename the `CONTCAR` file from the results of Step 3 to `POSCAR` and place it in the newly created `con` folder. It will then copy the three input files from the `Con_source` folder into each `con` folder. The resulting folder structure will be:
>
> ```
> "Tot_Band" Folder
> -----------------------------------------------------------------------------------
> D:.
> └─ Tot_Band
> 		  ├─Cr_O_Se_S
> 		  |    ├─input 
> 		  |    |    ├─ POTCAR
> 		  |    |       POSCAR 
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs
> 		  |    ├─opt
> 		  |    |    ├─ POTCAR  
> 		  |    |       POSCAR
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs  
> 		  |    |
> 		  |    ├─con
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs 
> 		  |         
>          ├─F_N_As_Te
>          |    ├─input
> 		  |    |    ├─ POTCAR
> 		  |    |       POSCAR 
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs
> 		  |    ├─opt
> 		  |    |    ├─ POTCAR  
> 		  |    |       POSCAR
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs  
> 		  |    |
> 		  |    ├─con
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs  
> 		  |
>          ├─Mo_Se_Te_Se    
>          |    ├─input
> 		  |    |    ├─ POTCAR
>          |    |       POSCAR
>          |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs
> 		  |    ├─opt
> 		  |    |    ├─ POTCAR  
> 		  |    |       POSCAR
> 		  |    |       INCAR
> 		  |    |       KPOINTS  
> 		  |    |       vasp.pbs  
> 		  |    |
> 		  |    ├─con
> 		  |        ├─ POTCAR  
> 		  |           POSCAR
> 		  |           INCAR
> 		  |           KPOINTS  
> 		  |           vasp.pbs  
>          .
>          ....
> -----------------------------------------------------------------------------------
> ```

> 2. **Run the `Sub_con.py` script to automatically submit the `vasp.pbs` job submission script in each `con` folder**.

### Step 5: Perform Band Structure Calculations
---

In this step, we do not create a `Band` folder; instead, we perform the calculations directly in the `con` folder.

> 1. **Run the `Band_incon.py` script to replace the `INCAR` and `KPOINTS` files in the `con` folder with those from the `Band_source` folder**.

> 2. **Run the `Sub_Band.py` script to automatically submit the `vasp.pbs` job submission script in each `con` folder (note that this is for band structure calculations)**.

---

#### TODO:

- [ ] Re-optimize the program
- [ ] Function refactoring and create an interface
 
