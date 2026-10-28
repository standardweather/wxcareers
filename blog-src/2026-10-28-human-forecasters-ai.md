---
title: Ensuring opportunities for human forecasters in the world of AI
date: 2026-10-28
description: "AI models are now operational at ECMWF and NOAA. Here is what they do well, where forecasters still matter, and how to build skills that last."
slug: human-forecasters-ai
draft: false
---

Every forecaster has had the same conversation lately: is the model going to do my job? The short answer from the people running the models is no. The longer answer is more useful, because it tells you where to put your effort. Everything below is sourced to the agencies and papers themselves, and any opinion is labeled as one.

## What the AI models do well

They are real, and they are operational. GraphCast, from Google DeepMind, [outperformed ECMWF's high-resolution deterministic model on 90% of 1,380 verification targets](https://www.science.org/doi/10.1126/science.adi2336) in its Science paper and produced a 10-day global forecast in under a minute. ECMWF [took its ensemble AIFS into operations on 1 July 2025](https://www.ecmwf.int/en/about/media-centre/news/2025/ecmwfs-ensemble-ai-forecasts-become-operational), 51 members running alongside the physics-based IFS, with gains of up to 20% on some measures such as surface temperature. It runs more than 10 times faster, and ECMWF says it uses roughly 1,000 times less energy.

NOAA followed in December 2025 with [AIGFS, AIGEFS and a hybrid ensemble called HGEFS](https://www.noaa.gov/news-release/noaa-deploys-new-generation-of-ai-driven-global-weather-models). A 16-day AIGFS run takes about 40 minutes on 0.3% of the computing resources of the operational GFS. NOAA reports that the hybrid ensemble, which combines 31 physics-based members with 31 AI members, consistently beats both the AI-only and physics-only ensembles. NOAA built its AI system on GraphCast, fine-tuned with its own analyses.

At the National Hurricane Center, 2025 was [the first season AI models were used in real-time operations](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf). In the Atlantic, the Google DeepMind ensemble mean slightly beat the official track forecast from 12 to 72 hours. That is a real result, and it would be silly to pretend otherwise.

## Where they still need a forecaster

The same documents are just as direct about limits. NHC's report says the official forecast outperformed most of the models and that some AI systems [were not consistently available on time](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf). NOAA's own release says AIGFS version 1.0 [degrades tropical cyclone intensity forecasts](https://www.noaa.gov/news-release/noaa-deploys-new-generation-of-ai-driven-global-weather-models). ECMWF's authors list [artefacts in mean sea level pressure, low effective resolution in cloud fields, and spurious patterns in accumulated precipitation](https://www.ecmwf.int/en/newsletter/185/earth-system-science/aifs-ens-becomes-operational) in AIFS ENS. ECMWF also says its 9 km physics-based ensemble ["remains indispensable for high-resolution fields"](https://www.ecmwf.int/en/about/media-centre/news/2025/ecmwfs-ensemble-ai-forecasts-become-operational), because AIFS ENS runs at 31 km.

Wallace Hogsett, NHC's Science Operations Officer, was asked whether AI will replace the hurricane forecaster. In [NHC's published Q&A](https://www.weather.gov/news/261102-AI-Hurricane-Forecasting) he called the answer "a resounding no" and added: "None of the models are perfect, and they never will be. Now more than ever, we need trusted experts in the loop." He also noted that AI and physics-based models make different kinds of errors, which helps forecasters see the full range of uncertainty.

The American Meteorological Society reached the same place in a January 2026 statement. It calls AI and machine learning [partners, not replacements](https://www.ametsoc.org/ams/about-ams/ams-statements/statements-of-the-ams-in-force/the-indispensable-role-of-people-in-the-weather-and-climate-forecast-value-chain/), says value comes when experts "discern which signals matter, recognize artifacts, and integrate socioeconomic considerations," and argues that the hard part now is the last mile, getting a forecast understood and acted on.

NWS forecasters have been asked directly, too. A [BAMS study of 29 NWS forecasters](https://doi.org/10.1175/bams-d-24-0044.1) found them tentatively open to AI/ML. Some worried it could replace them, but they were committed to the best possible forecasts with whatever tools help. The authors note that forecasters remain the sole authority for issuing watches and warnings.

## Where the opportunity is

This part is analysis, not a quoted finding. Models are getting better at the first questions: what is happening and how will it evolve. The jobs that grow in value sit on the other side of that.

**Decision support.** A faster, cheaper ensemble gives you more scenarios. Someone still has to turn them into a call for an emergency manager, a utility, an airline, or a school district. The AMS statement describes this work as [impact-based decision support and counsel that is interactive](https://www.ametsoc.org/ams/about-ams/ams-statements/statements-of-the-ams-in-force/the-indispensable-role-of-people-in-the-weather-and-climate-forecast-value-chain/), including caveats and questions, which a dashboard does not do.

**Model QC.** If you can tell when a model is confidently wrong, you are worth more now than before. The 2025 NHC numbers show a model can beat the official track at some ranges and still struggle with intensity. Knowing which tool to trust in which setup is a skill.

**Communication.** On-air, at a briefing, or on a warning, you are still the trusted voice. The AMS statement points to research showing viewers consider certified meteorologists ["highly trusted sources of information."](https://www.ametsoc.org/ams/about-ams/ams-statements/statements-of-the-ams-in-force/the-indispensable-role-of-people-in-the-weather-and-climate-forecast-value-chain/)

**Forensic and expert work.** BLS describes forensic meteorologists as people who [reconstruct weather conditions for a specific place and time](https://www.bls.gov/ooh/life-physical-and-social-science/atmospheric-scientists-including-meteorologists.htm) and may testify in court. That is built on observations of what happened, and on someone willing to put their name and methods on the record. Forecast models are not the main tool for that.

## What the labor numbers say, and what they don't

BLS puts median pay for atmospheric scientists at [$99,070 in May 2025](https://www.bls.gov/ooh/life-physical-and-social-science/atmospheric-scientists-including-meteorologists.htm), with about 10,700 jobs and 3% projected growth from 2025 to 2035, about average, and roughly 800 openings a year. Its employment section says new types of computer models have vastly improved forecast accuracy, which "should support demand" for atmospheric scientists as businesses want more specialized information. BLS also notes that growth at federal and publicly funded employers largely depends on funding. The page does not address AI specifically, so there is no sourced hiring trend to report.

## What to build

Published research points the same way. In [a BAMS paper on the evolving role of humans in forecasting](https://journals.ametsoc.org/view/journals/bams/103/8/BAMS-D-20-0326.1.xml), the authors name computing and data skills, probabilistic and ensemble forecasting, impact-based decision support, and communication. They also say that the federal GS-1340 requirements and AMS degree standards should be revised more often than they have been. If you are weighing the federal path, our [guide to NWS hiring on USAJOBS](https://wxcareers.com/blog/nws-jobs-usajobs/) covers the current 1340 coursework.

The practical version: learn to verify a model yourself, get comfortable with ensembles and probabilities, write code for the routine parts of your job, and practice explaining risk to someone who is not a meteorologist. Those skills carry over whether the guidance comes from a deterministic model, AI, or something that does not exist yet.

Browse current meteorology openings at https://wxcareers.com/.
