# RedHat x IBM Instruct Lab Bias Detection Model

This model trains [RedHat x IBM Instruct Lab](http://instructlab.ai/) to create a Bias Detection Model, using numerous taxonmies focusing on different types of biases to help identify bias in various forms of text. Upon reveiving the user's prompt, the model will identify any bias in the text, highlight the text and explain why the text provided is bias for the user to understand what to avoid to prevent bias in text. 

## Overview

InstructLab's model-agnostic technology gives model upstreams with sufficient infrastructure resources the ability to create regular builds of their open source licensed models not by rebuilding and retraining the entire model but by composing new skills into it.

## Results

| Original Model | Our Bias Detection Model |
|----------------|--------------------------|
| ---% Accuracy  | ---% Accuracy |

## Small Example

<img width="1241" height="745" alt="image" src="https://github.com/user-attachments/assets/bb29a09d-c53d-43c0-8b0f-36f52e2b8536" />

## Installation/How to run

1. Clone this repository 
2. [Install Instruct Lab for your system](https://docs.instructlab.ai/getting-started/mac_metal/) 
3. 

## Technologies Used

**IBM InstructLab** –------> for instruction-based model refinement and dataset generation

**Git** –-------------------> for version control and project management

**MT-Bench** –------------> for evaluating model performance

**Google Cloud Platform** –> for training and scalable compute

## Project Structure

**/data** ---------> Training and evaluation datasets  
**/models** ------> Model checkpoints or saved models  
**/src** ----------> Core model and processing code  
**/evaluation** ---> Benchmarking and testing scripts  
**README.md** -> Project documentation  

## Ethical Considerations

• The model addresses sensitive social concepts such as bias, discrimination, and stereotypes.

• There is a risk of false positives, where neutral or contextual language may be incorrectly flagged as biased.

• Over-reliance on the model may lead users to treat outputs as authoritative judgments rather than advisory feedback, which is not the intended use of this model.

• The model is designed to provide neutral explanations as much as possible within the capabilities of the developers to ensure the model is as unbiased as possible without accusatory or moralizing language.

• Bias detection outputs are intended to support reflection and revision, not punishment or exclusion.

## License

This project is licensed under the MIT License.

## Team

**CSC398 Group 1**

• Shaarif Ali Syed

• Asser Ismail

• Remy Zazo

• Zelimir Stajic

• Belal Shrief

University of Toronto

**Special Thanks**

Special thanks to our industry mentors Carol Chen and Wesly Chun, and to the RedHat x IBM Instruct Lab for the model, guidance, and reference material that made this work possible.

