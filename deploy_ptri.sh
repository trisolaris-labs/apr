#!/bin/bash

gcloud functions deploy gcc_ptri \
--entry-point gcc_ptri \
--runtime python39 \
--trigger-topic update_ptri.json \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
