#!/bin/bash

gcloud functions deploy gcc_apr \
--entry-point gcc_apr \
--runtime python37 \
--trigger-topic create_datav2.json \
--source https://source.developers.google.com/projects/trisolaris-ad-hoc/repos/github_trisolaris-labs_apr/moveable-aliases/master \
--project trisolaris-ad-hoc
