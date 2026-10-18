# Correlates of protection as a route to vaccine dose and regimen optimisation

## The empirical pathway

There is a recognisable default **empirical workflow**, although there is no single default statistical model. The strongest version starts inside a randomised efficacy trial. Specimens are collected at prespecified post-vaccination times, immune markers are measured among participants who are still event-free, and subsequent infection or disease is related to those measurements. Often the laboratory work uses a nested case–cohort design: assay all or most subsequent cases plus a random subcohort rather than the entire trial. Qin et al.'s useful hierarchy distinguishes an ordinary **correlate of risk** from a **surrogate of protection** that can predict vaccine effects; this distinction is central because an immune marker can be strongly prognostic without being sufficient for extrapolating the efficacy of a changed vaccine regimen. citeturn0search0turn0search15

Let \(M\) be an immune measurement at a landmark time \(\tau\), and \(Y\) subsequent disease. The first analysis is essentially

\[
P(Y=1\mid M=m,\;V=1,\;Y(\tau)=0,\;X),
\]

or its time-to-event analogue. A declining risk curve with increasing \(m\) establishes an individual-level correlate of risk. Because \(M\) is post-randomisation and is not itself randomised, however, this association need not be causal: high responders can differ in age, health, exposure, or other immune responses. Baseline-risk adjustment, two-phase sampling weights, and designs using baseline predictors of the immune response help, but they do not turn an observational marker–outcome association into a causal surrogate automatically. citeturn0search0turn0search15

For **immunobridging**, what is needed is stronger: evidence that a specified immune response carries sufficiently stable information about protection that efficacy results from one population or regimen can be transported to another. Evidence becomes more persuasive when the marker–protection relationship reproduces across trials, populations, doses or vaccine platforms, and when interventions that shift the marker also shift clinical efficacy in the predicted direction. Qin et al. call these progressively stronger forms of surrogacy; the important statistical point is that *individual-level prediction is weaker evidence than intervention-level prediction*. citeturn0search0

## How the correlate is used for dose optimisation

In practice, the most common bridge is simpler than fitting a precise titre-to-efficacy equation. A candidate lower dose, longer interval or reduced-dose schedule is randomised against a regimen whose efficacy is already established, and a prespecified immune endpoint is tested for **non-inferiority**. Depending on the vaccine, the endpoint may be a geometric mean titre or concentration, the proportion above a reference concentration, a seroresponse rate, or a functional assay. If the immune response satisfies the agreed margin, comparable clinical protection is inferred under the bridging assumptions rather than re-estimated from thousands of clinical endpoints. Pneumococcal conjugate vaccines are a particularly mature example: WHO criteria permit immunogenicity comparison with a licensed PCV, and the historical \(0.35\,\mu\text{g}/\text{mL}\) anti-capsular IgG reference concentration was derived from efficacy data and used in vaccine-comparison criteria. Importantly, WHO's framework treats this as a **population-level reference value**, not a deterministic threshold that guarantees protection in an individual. citeturn0search1turn0search9

There is a more quantitative version. Suppose an efficacy trial has estimated a conditional clinical-risk function \(r(m,x)\), and a small dose-ranging study estimates the immune-response distribution \(F_g(m\mid x)\) under candidate regimen \(g\). One can predict clinical risk approximately by standardisation:

\[
R_g \approx \int r(m,x)\,dF_g(m\mid x)\,dF_{\rm target}(x),
\]

and, given a contemporaneous unvaccinated risk \(R_0\),

\[
VE_g \approx 1-\frac{R_g}{R_0}.
\]

Thus the whole **distribution** of responses from the small trial is passed through the previously estimated marker–risk curve. A threshold model is the limiting special case, where efficacy depends mainly on \(P(M>c)\). Continuous curves are generally more realistic.

The mRNA-1273 COVE trial illustrates this approach unusually clearly. Binding and neutralising antibodies measured after vaccination were inversely related to later COVID-19 risk, and estimated vaccine efficacy rose across the neutralising-antibody range: for post-vaccination neutralisation titres of 10, 100 and 1,000, estimated efficacy was approximately 78%, 91% and 96%, respectively. The analysis therefore supplied a graded protection curve rather than a single protective cut-off. citeturn0search7turn0search11 Cross-vaccine modelling by Khoury et al. similarly found that standardised neutralisation levels were strongly predictive of phase III efficacy and obtained useful leave-one-vaccine-out predictions, showing the form that a genuinely quantitative immunogenicity-to-efficacy bridge can take. citeturn1search2

A correlate need not have an accepted absolute protective threshold to be useful. The nine-valent HPV programme is a good example. In a 1,518-participant immunogenicity trial, two doses in girls and boys aged 9–14 years, separated by either six or 12 months, produced HPV-type-specific antibody GMTs non-inferior to those after three doses in 16–26-year-old females from the population in which protection had been demonstrated. The prespecified non-inferiority margin for the GMT ratio was 0.67. The investigators explicitly used this as an immunobridge even though a minimum protective HPV antibody titre had not been established. citeturn1search0 This is an important practical distinction: **bridging to the immune response of an efficacious reference regimen can require less than knowing an absolute correlate of protection**.

## Waning and protection over time

A single peak response only supports inference over a period for which its relation to later disease has been established. For optimisation over longer horizons, the problem is longitudinal. If \(M_g(t)\) denotes the marker trajectory under regimen \(g\), a natural model relates instantaneous disease hazard to the current or recent immune response,

\[
\lambda_g(t\mid X)
 = \lambda_0(t\mid X)\exp\{f[M_g(t),t,X]\},
\]

and integrates that hazard to obtain cumulative risk. Candidate regimens can then differ in their peak response, decay rate and timing of boosting. Repeated samples in dose-ranging studies are therefore substantially more informative than a single peak GMT when the policy question concerns duration of protection.

There are two distinct extrapolations here. The first is **immune kinetics**: whether the lower-dose or altered schedule has the same decay form after allowing for a different starting level. The second is **protection conditional on immunity**: whether a titre of, say, 100 has the same meaning at month 18 as at month two and under the circulating pathogen strains represented in the efficacy data. SARS-CoV-2 illustrates both the potential and limitation of this strategy: neutralisation was a strong correlate within COVE and across early vaccine trials, while large antigenic changes could substantially alter neutralisation of the circulating virus, so the relevant marker must be measured against an antigenically appropriate strain rather than treated as an invariant laboratory quantity. citeturn0search5turn0search11turn1search2

Consequently, a durability bridge may compare candidate and reference regimens at several landmarks or jointly model their antibody trajectories. A candidate regimen with a slightly lower peak but slower decline could have similar or greater integrated protection; conversely, peak non-inferiority says comparatively little about long-term efficacy if decay rates differ.

## The assumptions behind translating immunogenicity into efficacy

For a small immunogenicity study to substitute credibly for a new efficacy trial, four assumptions do most of the work.

**First, conditional transportability.** After conditioning on the immune marker and relevant covariates, clinical risk must be approximately independent of which dose or regimen generated that marker. In notation,

\[
P(Y\mid M,X,g_{\rm new})
   \simeq P(Y\mid M,X,g_{\rm reference}).
\]

This is the central assumption behind plugging a new regimen's \(F_g(M)\) into an old protection curve. It is stronger than showing that \(M\) predicts disease in the original trial. citeturn0search0

**Second, the marker must capture the relevant regimen-induced differences.** Two regimens can produce the same antibody concentration yet differ in neutralising activity, affinity, epitope breadth, Fc-mediated functions, mucosal immunity, memory responses or cellular immunity. If those differences independently affect protection, equal values of \(M\) do not imply equal efficacy. Immunobridging is therefore strongest when the changed dose or schedule plausibly changes mainly the *amount or duration* of a well-validated response, and weaker when it could change its composition.

**Third, measurement and biological context must transport.** Assays need sufficient calibration and comparability, and the efficacy data need to be relevant to the target population, endpoint and pathogen. The pneumococcal framework makes assay comparability explicit: its reference concentration is tied to a specified ELISA methodology, with alternative assays requiring bridging. citeturn0search9

**Fourth, the comparator must anchor clinical efficacy.** Immune non-inferiority is most informative when the reference immune distribution comes from a regimen with demonstrated protection. This is exactly the logic of both WHO's pneumococcal criteria and the HPV two-dose study. citeturn0search1turn1search0

These assumptions also explain why varying the **interval** can be less straightforward than simply lowering antigen quantity. In the HPV study, for example, antibody responses depended on the spacing of the two doses, with the 12-month interval generally producing higher responses than the six-month interval. citeturn1search0 Altering timing can change maturation and durability as well as the measured peak; therefore a bridge based on one post-dose measurement implicitly asserts that those additional changes do not alter protection conditional on that measurement.

## Why TB is different

TB illustrates the other end of the spectrum. Studies can identify immune variables that predict subsequent disease without thereby obtaining a surrogate suitable for regimen optimisation. Fletcher et al., analysing BCG-vaccinated infants, identified **T-cell activation as an immune correlate of subsequent TB risk**. That is scientifically useful, but in Qin et al.'s terminology it is a correlate of risk rather than, by itself, a validated intervention-level surrogate of protection. citeturn1search3turn0search0

The practical consequence is large. For pneumococcal or HPV vaccines, researchers can ask whether a new schedule reproduces an immune response already tied to successful clinical protection. For TB, an observed difference in a candidate regimen's T-cell response cannot in general be converted into a defensible numerical difference in TB efficacy, because it has not been established that interventions which alter that response produce the corresponding change in clinical disease. The missing step is therefore not simply a more precise assay; it is validation of the **intervention-level relationship between changes in immunity and changes in protection**. citeturn1search3turn0search0

## Bottom line

The closest thing to a default model is therefore:

\[
\text{efficacy trial}
\rightarrow
\text{post-vaccination marker}
\rightarrow
\text{marker--future-risk curve}
\rightarrow
\text{validation across interventions/settings}
\rightarrow
\text{immunobridge}.
\]

But the steps should not be collapsed. A marker associated with risk is the first empirical result; a validated surrogate capable of predicting the effect of changing dose or regimen is a substantially stronger result. citeturn0search0

Once that stronger bridge exists, dose optimisation can proceed either by **immune non-inferiority** to an efficacious regimen—the common regulatory design—or by combining a calibrated marker–protection curve with the immune-response distribution observed in a small randomised dose-ranging study. Pneumococcal vaccines illustrate a mature reference-concentration framework; HPV shows that useful immunobridging is possible even without an absolute protective threshold; COVID-19 provides an unusually explicit continuous antibody-to-efficacy relationship. TB demonstrates the limiting case: correlates of risk exist, but without sufficiently validated intervention-level surrogacy, small immunogenicity studies cannot yet be translated reliably into predicted clinical efficacy. citeturn0search9turn1search0turn0search11turn1search3