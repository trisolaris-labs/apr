#!/bin/bash

gcloud functions deploy gcc_ptri_fees \
--entry-point gcc_ptri_fees \
--runtime python39 \
--trigger-topic gcc_ptri_fees \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
