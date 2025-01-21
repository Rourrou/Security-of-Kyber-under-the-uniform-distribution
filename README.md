# Data and Code for the work "On the Security of LWE-based KEMs under Various Distributions: A Case Study of Kyber"
https://eprint.iacr.org/2024/1979

Section 3. Kyber hardness
1. Compute the hardness of Kyber and its variant under the uniform distribution: set the distr parameter in MLWE_security with "binomial" or "uniform" and run Kyber_hardness.py

Section 4. Decryption failure attack
1. Compute the decryption failure probability of Kyber and its variant under the uniform distribution: run Kyber_failure.py
2. Collect the failures: the decryption failures are collected as Kyber512_uniform/decryption_failures_33322_all.txt
3. Identify the sign and position of failure: run df_position.py
4. Recovering the secret key using decryption failures: run key_recovery.py 
    

