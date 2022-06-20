#!/bin/bash

gcloud functions deploy gcc_ptri_v2 \
--entry-point gcc_ptri_v2 \
--runtime python39 \
--trigger-topic update_ptri_v2.json \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
