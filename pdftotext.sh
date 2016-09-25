#!/bin/bash
ls -1 *.pdf | parallel -j 10 pdftotext