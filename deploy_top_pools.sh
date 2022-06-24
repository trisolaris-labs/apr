#!/bin/bash

gcloud functions deploy gcc_top_pools \
--entry-point gcc_top_pools \
--runtime python39 \
--trigger-topic update_pools.json \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
