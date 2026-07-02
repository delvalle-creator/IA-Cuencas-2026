<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.0-Prizren" styleCategories="AllStyleCategories">
  <pipe>
    <provider>
      <resamplingStage>resamplingFilter</resamplingStage>
      <enabled>true</enabled>
      <zoomedInResamplingMethod>bilinear</zoomedInResamplingMethod>
      <zoomedOutResamplingMethod>average</zoomedOutResamplingMethod>
      <maxOversampling>2</maxOversampling>
    </provider>
    <rasterrenderer type="singlebandpseudocolor" band="1" classificationMin="0" classificationMax="3" opacity="1" alphaBand="-1" nodataColor="">
      <rasterTransparency>
        <singleValuePixelList>
          <pixelListEntry min="-9999" max="0.05" percentTransparent="100"/>
        </singleValuePixelList>
      </rasterTransparency>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" classificationMode="1" clip="0" minimumValue="0" maximumValue="3" labelPrecision="2">
          <item value="0.05" color="#c6dbef" label="0,05 m" alpha="255"/>
          <item value="0.5"  color="#6baed6" label="0,5 m" alpha="255"/>
          <item value="1"    color="#3182bd" label="1,0 m" alpha="255"/>
          <item value="2"    color="#08519c" label="2,0 m" alpha="255"/>
          <item value="3"    color="#08306b" label="≥ 3,0 m" alpha="255"/>
          <rampLegendSettings minimumLabel="" maximumLabel="" prefix="" suffix=" m" orientation="2" direction="0" useContinuousLegend="1">
            <numericFormat id="basic"/>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation invertColors="0" colorizeStrength="100" colorizeOn="0" colorizeBlue="128" saturation="0" colorizeGreen="128" grayscaleMode="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
