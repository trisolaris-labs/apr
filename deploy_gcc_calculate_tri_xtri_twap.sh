#!/bin/bash

gcloud functions deploy gcc_calculate_tri_xtri_twap \
--entry-point gcc_calculate_tri_xtri_twap \
--runtime python39 \
--trigger-topic update_tri_xtri_twap \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
