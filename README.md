# Deep learning for cancer therapy

# Motivation:  
Machine learning can be used to perform unsupervised learning on the DNA sequences of patient tumors in order to  identify non-linear features of the tumor DNA that help predict treatment.  

# Goal:  
To use deep learning to identify patients whose tumor DNA mutations “look similar to” other tumors for which treatments are effective.  

# Approach:  
Convolutional neural networks (CNN) have led to substantial advances in both supervised and unsupervised learning tasks in computer vision. It is easy to treat DNA sequence (an ordered sequence of A’s, C’s, G’s, and T’s) as an “image”, and therefore apply many of the same techniques used in imaging to DNA sequence.  

# Deliverables:
Software implementing a CNN that can take in DNA sequences from multiple patient tumors, and produce two visualizations: (1) a lower dimensional (2D) projection of individual mutations from multiple patients, to be used for unsupervised clustering of mutations; and (2) a lower dimensional (2D) projection of individuals (based on their total set of mutations), for identifying patients whose tumors look like other patients whose treatments are known to be effective.  

# Platforms: 
TensorFlow, Python, skl. 
  
# Team & Contact:  
Suraj Jena <skjena@ucdavis.edu>,
Kumud Ravisankaran <kravisankaran@ucdavis.edu>,
Valeria Brewer <valramirez@ucdavis.edu>,
Ninad Mehta <ntmehta@ucdavis.edu>,
