#!/bin/bash

gcloud functions deploy gcc_xtri \
--entry-point gcc_xtri \
--runtime python37 \
--trigger-topic update_xtri.json \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
