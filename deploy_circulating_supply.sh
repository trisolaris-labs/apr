#!/bin/bash

gcloud functions deploy gcc_total_circulating_supply \
--entry-point gcc_total_circulating_supply \
--runtime python39 \
--trigger-topic calculate_circulating_supply \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
