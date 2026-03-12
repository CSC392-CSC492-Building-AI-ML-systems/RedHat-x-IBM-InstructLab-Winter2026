In the field of statistics, bias is a systematic tendency in which the methods used to gather data and estimate a sample statistic present an inaccurate, skewed or distorted (biased) depiction of reality. Statistical bias exists in numerous stages of the data collection and analysis process, including: the source of the data, the methods used to collect the data, the estimator chosen, and the methods used to analyze the data.

Data analysts can take various measures at each stage of the process to reduce the impact of statistical bias in their work. Understanding the source of statistical bias can help to assess whether the observed results are close to actuality. Issues of statistical bias has been argued to be closely linked to issues of statistical validity.[1]

Statistical bias can have significant real world implications as data is used to inform decision making across a wide variety of processes in society. Data is used to inform lawmaking, industry regulation, corporate marketing and distribution tactics, and institutional policies in organizations and workplaces. Therefore, there can be significant implications if statistical bias is not accounted for and controlled. For example, if a pharmaceutical company wishes to explore the effect of a medication on the common cold but the data sample only includes men, any conclusions made from that data will be biased towards how the medication affects men rather than people in general. That means the information would be incomplete and not useful for deciding if the medication is ready for release in the general public. In this scenario, the bias can be addressed by broadening the sample. This sampling error is only one of the ways in which data can be biased.

Bias can be differentiated from other statistical mistakes such as accuracy (instrument failure/inadequacy), lack of data, or mistakes in transcription (typos). Bias implies that the data selection may have been skewed by the collection criteria. Other forms of human-based bias emerge in data collection as well such as response bias, in which participants give inaccurate responses to a question. Bias does not preclude the existence of any other mistakes. One may have a poorly designed sample, an inaccurate measurement device, and typos in recording data simultaneously. Ideally, all factors are controlled and accounted for.

Also it is useful to recognize that the term “error” specifically refers to the outcome rather than the process (errors of rejection or acceptance of the hypothesis being tested), or from the phenomenon of random errors.[2] The terms flaw or mistake are recommended to differentiate procedural errors from these specifically defined outcome-based terms.

Bias of an estimator
Main article: Bias of an estimator
Statistical bias is a feature of a statistical technique or of its results whereby the expected value of the results differs from the true underlying quantitative parameter being estimated. The bias of an estimator of a parameter should not be confused with its degree of precision, as the degree of precision is a measure of the sampling error. The bias is defined as follows: let 
T
{\displaystyle T} be a statistic used to estimate a parameter 
θ
{\displaystyle \theta }, and let 
E
⁡
(
T
)
{\displaystyle \operatorname {E} (T)} denote the expected value of 
T
{\displaystyle T}. Then,

bias
⁡
(
T
,
θ
)
=
bias
⁡
(
T
)
=
E
⁡
(
T
)
−
θ
{\displaystyle \operatorname {bias} (T,\theta )=\operatorname {bias} (T)=\operatorname {E} (T)-\theta }
is called the bias of the statistic 
T
{\displaystyle T} (with respect to 
θ
{\displaystyle \theta }). If 
bias
⁡
(
T
,
θ
)
=
0
{\displaystyle \operatorname {bias} (T,\theta )=0}, then 
T
{\displaystyle T} is said to be an unbiased estimator of 
θ
{\displaystyle \theta }; otherwise, it is said to be a biased estimator of 
θ
{\displaystyle \theta }.

The bias of a statistic 
T
{\displaystyle T} is always relative to the parameter 
θ
{\displaystyle \theta } it is used to estimate, but the parameter 
θ
{\displaystyle \theta } is often omitted when it is clear from the context what is being estimated.

Types
Statistical bias comes from all stages of data analysis. The following sources of bias will be listed in each stage separately.

Data selection
Selection bias involves individuals being more likely to be selected for study than others, biasing the sample. This can also be termed selection effect, sampling bias and Berksonian bias.[3]

Spectrum bias arises from evaluating diagnostic tests on biased patient samples, leading to an overestimate of the sensitivity and specificity of the test. For example, a high prevalence of disease in a study population increases positive predictive values, which will cause a bias between the prediction values and the real ones.[4]
Observer selection bias occurs when the evidence presented has been pre-filtered by observers, which is so-called anthropic principle. The data collected is not only filtered by the design of experiment, but also by the necessary precondition that there must be someone doing a study.[5] An example is the impact of the Earth in the past. The impact event may cause the extinction of intelligent animals, or there were no intelligent animals at that time. Therefore, some impact events have not been observed, but they may have occurred in the past.[6]
Volunteer bias occurs when volunteers have intrinsically different characteristics from the target population of the study.[7] Research has shown that volunteers tend to come from families with higher socioeconomic status.[8] Furthermore, another study shows that women are more probable to volunteer for studies than men.[9]
Funding bias may lead to the selection of outcomes, test samples, or test procedures that favor a study's financial sponsor.[10]
Attrition bias arises due to a loss of participants, e.g., loss of follow up during a study.[11]
Recall bias arises due to differences in the accuracy or completeness of participant recollections of past events; for example, patients cannot recall how many cigarettes they smoked last week exactly, leading to over-estimation or under-estimation.
Hypothesis testing
See also: Uniformly most powerful test
In the Neyman–Pearson framework, the goodness of a hypothesis test is determined by its type I and type II errors.[12] Type I error, or false positive, happens when the null hypothesis is correct but is rejected. The false positive rate is written as 
α
{\displaystyle \alpha }. Type II error, or false negative, happens when the null hypothesis is not correct but is accepted. The false negative rate is written as 
β
{\displaystyle \beta }.

For instance, suppose that speeding is defined as having average driving speed limit is below 85 km/h, and let the null hypothesis be "not speeding". If someone receives a ticket with an average driving speed of 70 km/h, the decision maker has committed a Type I error. Conversely, if someone does not receive a ticket with an average driving speed of 90 km/h, the decision maker has committed a Type II error.

Generally, a statistical test may decrease 
α
{\displaystyle \alpha }, but possibly at the price of increasing 
β
{\displaystyle \beta }, and vice versa. For example, the test may be very sensitive to true positives, but at the price of creating many false positives, and vice versa. Furthermore, whereas 
α
{\displaystyle \alpha } depends on just the statistical test itself and the null hypothesis 
H
0
{\displaystyle H_{0}}, 
β
{\displaystyle \beta } depends on the statistical test and an unknown alternative hypothesis 
H
1
{\displaystyle H_{1}}. The Neyman–Pearson framework bypasses the difficulty with having an unknown 
H
1
{\displaystyle H_{1}} by imposing a kind of uniformity. That is, tests are good iff they work well on any 
H
1
{\displaystyle H_{1}}.

Formally, define the following:

H
0
{\displaystyle H_{0}}, a null hypothesis.
T
{\displaystyle \mathrm {T} }, a test.
Using the previous definitions, we have
Pr
(
reject 
H
0
|
H
0
,
T
)
=
α
(
H
0
,
T
)
,
Pr
(
reject 
H
0
|
H
1
,
T
)
=
1
−
β
(
H
1
,
T
)
{\displaystyle \Pr({\text{reject }}H_{0}|H_{0},\mathrm {T} )=\alpha (H_{0},\mathrm {T} ),\quad \Pr({\text{reject }}H_{0}|H_{1},\mathrm {T} )=1-\beta (H_{1},\mathrm {T} )}
where 
H
1
{\displaystyle H_{1}} is an unspecified alternative hypothesis.

We say that the test is unbiased (in the Neyman–Pearson sense) iff for any alternative hypothesis 
H
1
{\displaystyle H_{1}},
Pr
(
reject 
H
0
|
H
1
,
T
)
≥
α
(
H
0
,
T
)
{\displaystyle \Pr({\text{reject }}H_{0}|H_{1},\mathrm {T} )\geq \alpha (H_{0},\mathrm {T} )}
Note that the right side of the equation cannot possibly be greater than 
α
(
H
0
,
T
)
{\displaystyle \alpha (H_{0},\mathrm {T} )}, because this formalism allows 
H
1
{\displaystyle H_{1}} to be exactly the same as 
H
0
{\displaystyle H_{0}}, in which case
Pr
(
reject 
H
0
|
H
1
,
T
)
=
α
(
H
0
,
T
)
{\displaystyle \Pr({\text{reject }}H_{0}|H_{1},\mathrm {T} )=\alpha (H_{0},\mathrm {T} )}
In short: an unbiased test is a test that minimizes the maximal false negative rate over all alternative hypotheses.

Generally, one considers not a single test, but an entire family of tests, using a test statistic. Let 
T
{\displaystyle T} be a test statistic. For each significance level 
p
∈
[
0
,
1
]
{\displaystyle p\in [0,1]}, the corresponding test is to check whether 
T
>
p
{\displaystyle T>p}. If so, then the null hypothesis is rejected at significance level 
p
{\displaystyle p}. Otherwise, it is accepted.

We say that the test statistic (or the family of tests) is unbiased (in the Neyman–Pearson sense) iff for any significance level 
p
{\displaystyle p}, it is unbiased.[12]: 6 [13]

Estimator selection
The bias of an estimator is the difference between an estimator's expected value and the true value of the parameter being estimated. Although an unbiased estimator is theoretically preferable to a biased estimator, in practice, biased estimators with small biases are frequently used. A biased estimator may be more useful for several reasons. First, an unbiased estimator may not exist without further assumptions. Second, sometimes an unbiased estimator is hard to compute. Third, a biased estimator may have a lower value of mean squared error.

A biased estimator is better than any unbiased estimator arising from the Poisson distribution.[14][15] The value of a biased estimator is always positive and the mean squared error of it is smaller than the unbiased one, which makes the biased estimator be more accurate.
Omitted-variable bias is the bias that appears in estimates of parameters in regression analysis when the assumed specification omits an independent variable that should be in the model.
Analysis methods
Detection bias occurs when a phenomenon is more likely to be observed for a particular set of study subjects. For instance, the syndemic involving obesity and diabetes may mean doctors are more likely to look for diabetes in obese patients than in thinner patients, leading to an inflation in diabetes among obese patients because of skewed detection efforts.
In educational measurement, bias is defined as "Systematic errors in test content, test administration, and/or scoring procedures that can cause some test takers to get either lower or higher scores than their true ability would merit."[16] The source of the bias is irrelevant to the trait the test is intended to measure.
Observer bias arises when the researcher subconsciously influences the experiment due to cognitive bias where judgment may alter how an experiment is carried out / how results are recorded.
Interpretation
Reporting bias involves a skew in the availability of data, such that observations of a certain kind are more likely to be reported.

Addressing statistical bias
Depending on the type of bias present, researchers and analysts can take different steps to reduce bias on a data set. All types of bias mentioned above have corresponding measures which can be taken to reduce or eliminate their impacts.

Bias should be accounted for at every step of the data collection process, beginning with clearly defined research parameters and consideration of the team who will be conducting the research.[2] Observer bias may be reduced by implementing a blind or double-blind technique. Avoidance of p-hacking is essential to the process of accurate data collection. One way to check for bias in results after is rerunning analyses with different independent variables to observe whether a given phenomenon still occurs in dependent variables.[17] Careful use of language in reporting can reduce misleading phrases, such as discussion of a result "approaching" statistical significant as compared to actually achieving it.[2]