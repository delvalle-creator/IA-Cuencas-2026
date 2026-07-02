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
    <rasterrenderer type="singlebandpseudocolor" band="1" classificationMin="0" classificationMax="80" opacity="1" alphaBand="-1" nodataColor="">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" classificationMode="1" clip="0" minimumValue="0" maximumValue="80" labelPrecision="0">
          <item value="0"  color="#08519c" label="0 m (más bajo)" alpha="255"/>
          <item value="2"  color="#3182bd" label="2 m" alpha="255"/>
          <item value="5"  color="#6baed6" label="5 m" alpha="255"/>
          <item value="10" color="#a1d99b" label="10 m" alpha="255"/>
          <item value="20" color="#ffffbf" label="20 m" alpha="255"/>
          <item value="35" color="#fdae61" label="35 m" alpha="255"/>
          <item value="50" color="#f46d43" label="50 m" alpha="255"/>
          <item value="65" color="#b15928" label="65 m" alpha="255"/>
          <item value="80" color="#ffffff" label="80 m (más alto)" alpha="255"/>
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
