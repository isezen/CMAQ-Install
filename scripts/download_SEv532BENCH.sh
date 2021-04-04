#! /bin/bash

# Download SEv5.3.2.BENCH files from Google Drive
# https://drive.google.com/drive/folders/1jAKw1EeEzxLSsmalMplNwYtUv08pwUYk
# Requirements: pip install gdown
# isezen
# 2021-03-31

if ! command -v gdown &> /dev/null
then
    echo "pip install gdown"
    exit 1
fi

folder=SEv532BENCH

mkdir -p $folder/WRFv4.1.1-CMAQv5.3.2

cd $folder

# GRIDMASK_STATES_12SE1.nc
gdown --id 16JJ4d6ChBJsvMc_ErqwDBrFfGh2MnVYR

# CMAQv5.3.2_Benchmark_2Day_Input.tar.gz.list
gdown --id 1LgJDD6-LTAJ7cPXpMeaTFDedsQAo1HBK

# CMAQv5.3.2_Benchmark_2Day_Input.tar.gz
gdown --id 1ex6Wr4dX6a0fgaDfhO0VEJNaCKqOflI5

# CMAQv5.3.2_Benchmark_2Day_Output_Optimized.tar.gz.list
gdown --id 1Ko8lC_53SUv7GFJ-0mnaWS0p1ix4b9J7

# CMAQv5.3.2_Benchmark_2Day_Output_Optimized.tar.gz
gdown --id 1HLNLiwNovAG82Zgb4zA1LcRyqhqvnwq4

# CMAQv5.3.2_Benchmark_2Day_Output_Debug.tar.gz.list
gdown --id 1czLfWtnIihQQcnws4ycmrMyHyTuSa6Jo

# CMAQv5.3.2_Benchmark_2Day_Output_Debug.tar.gz
gdown --id 1WWxlgQFuBgaIDFHbdZWukElDqPBTsf3x

# ------------------------------------------
# WRFv4.1.1-CMAQv5.3.2 Folder
cd WRFv4.1.1-CMAQv5.3.2

# WRFv4.1.1-CMAQv5.3.2_rel_debug_output_12km_nf_rrtmg_20_5_1_v411532_16pe_2day.tar.gz.list
gdown --id 1B0IW3yMdAjkn2VWPq2NUVJpELfmIlhOq

# WRFv4.1.1-CMAQv5.3.2_rel_debug_output_12km_nf_rrtmg_20_5_1_v411532_16pe_2day.tar.gz
gdown --id 1QdHQGpP1lWUgGZbxZ-V64d_rgmg0YFbQ

# WRFv4.1.1-CMAQv5.3.2_rel_debug_output_12km_sf_rrtmg_20_5_1_v411532_32pe_2day.tar.gz.list
gdown --id 1wLiI_z5RDlgBec73BEPY2AqkXlPr1ZZ_

# WRFv4.1.1-CMAQv5.3.2_rel_debug_output_12km_sf_rrtmg_20_5_1_v411532_32pe_2day.tar.gz
gdown --id 14ygQOoeWaolwecZE0nS00xjRbG5bhznA

# WRFv4.1.1-CMAQv5.3.2_opt_output_12km_sf_rrtmg_20_5_1_v411532_16pe_2day.tar.gz.list
gdown --id 1uty_MkEBucgtCgU93BDLOpsp9rvF4QKf

# WRFv4.1.1-CMAQv5.3.2_opt_output_12km_sf_rrtmg_20_5_1_v411532_16pe_2day.tar.gz
gdown --id 1vHPYJDRXNnsbXw058i-48OTmNNAxLtYI

# WRFv4.1.1-CMAQv5.3.2_opt_output_12km_nf_rrtmg_20_5_1_v411532_16pe_2day.tar.gz.list
gdown --id 17Ry2aLy17GfN9p_T7BYnUvQEZkft05wY

# WRFv4.1.1-CMAQv5.3.2_opt_output_12km_nf_rrtmg_20_5_1_v411532_16pe_2day.tar.gz
gdown --id 1YasJI6LWtk_HKCJzikVSShAW2SecmbG_

# WRFv4.1.1-CMAQv5.3.2_twoway.tar.gz.list
gdown --id 1_Xx0pi8j2AQV7snS_YVFaR_XOvgcdejE

# readme-wrf-cmaq.10_2020.txt
gdown --id 1K7nnzdazj3N5lzuHRc_Px2w7kheK73a1

# WRFv4.1.1-CMAQv5.3.2_twoway.tar.gz
gdown --id 1oZecf-4aRu9q0ZptNsyI63QU4KUrTFFl

cd ../..
