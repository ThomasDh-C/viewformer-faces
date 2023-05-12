# FaceShift
- Download all face data from https://fei.edu.br/~cet/facedatabase.html
- Create necessary conda environments (see https://github.com/jkulhanek/viewformer, https://researchcomputing.princeton.edu/support/knowledge-base/pytorch and https://researchcomputing.princeton.edu/support/knowledge-base/tensorflow). Note to use python 3.8
- To get all poses data run data.py
- To download all test data from viewformer paper run every cell in viewformer-playground.ipynb
- To visualise this data and generate necessary data for custom data in viewformer use data_explorer.ipynb
- To visualise adjusting a single pose use visualise_single_pose_change.ipynb
- To fine-tune a codebook or transformer reference test_codebook_train.ipynb, codebook_finetune.slurm and train_transformer.slurm
- Finally, after running all the above, to use the custom datasets you have generated and the new viewformer architectures run viewformer-face-playground.ipynb
