#!/usr/bin/env bash
tar -czf ~/Mulle_${BUILD_LANG}.tgz ${TRAVIS_BUILD_DIR}/dist
tar -czf ~/Mulle_cst_${BUILD_LANG}.tgz ${TRAVIS_BUILD_DIR}/cst_out_new
