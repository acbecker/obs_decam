#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.afw.table as afwTable
import lsst.afw.image as afwImage
import lsst.afw.cameraGeom as afwCameraGeom
import lsst.afw.geom as afwGeom
from lsst.pipe.tasks.processImage import ProcessImageTask

class ProcessCcdDecamConfig(ProcessImageTask.ConfigClass):
    """Config for ProcessCcdDecam"""
    pass

class ProcessCcdDecamTask(ProcessImageTask):
    """Process a CCD for SDSS
    """
    ConfigClass = ProcessCcdDecamConfig
    _DefaultName = "processCcd"
    dataPrefix = ""

    def __init__(self, **kwargs):
        ProcessImageTask.__init__(self, **kwargs)

    @classmethod
    def _makeArgumentParser(cls):
        return pipeBase.ArgumentParser(name=cls._DefaultName, datasetType="raw")        

    def makeIdFactory(self, sensorRef):
        expBits = 24
        expId = long(sensorRef.dataId["visit"])
        return afwTable.IdFactory.makeSource(expId, 64 - expBits)

    @pipeBase.timeMethod
    def run(self, sensorRef):
        """Process a CCD: including source detection, photometry and WCS determination
        
        @param sensorRef: sensor-level butler data reference to SDSS fpC file
        @return pipe_base Struct containing these fields:
        - exposure: calibrated exposure (calexp): as computed if config.doCalibrate,
            else as upersisted and updated if config.doDetection, else None
        - calib: object returned by calibration process if config.doCalibrate, else None
        - apCorr: aperture correction: as computed config.doCalibrate, else as unpersisted
            if config.doMeasure, else None
        - sources: detected source if config.doPhotometry, else None
        """
        self.log.info("Processing %s" % (sensorRef.dataId))
        exp = sensorRef.get("raw")

        # delegate most of the work to ProcessImageTask
        result = self.process(sensorRef, exp)
        return result

