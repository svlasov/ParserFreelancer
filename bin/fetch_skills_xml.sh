#!/usr/bin/env bash
curl https://www.freelancer.com/sitemap/default/jobs-1.xml.gz | gunzip -> ${PWD}/data/skills.xml
