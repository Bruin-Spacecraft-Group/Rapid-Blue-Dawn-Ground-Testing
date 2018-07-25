<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="font">
   <font>
    <family>Arial Narrow</family>
    <pointsize>10</pointsize>
   </font>
  </property>
  <property name="windowTitle">
   <string>Rapid GSE</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="gridLayoutWidget">
    <property name="geometry">
     <rect>
      <x>9</x>
      <y>9</y>
      <width>381</width>
      <height>421</height>
     </rect>
    </property>
    <layout class="QGridLayout" name="gridLayout" rowstretch="0,0,0,0,0" columnstretch="0,0">
     <item row="4" column="0">
      <widget class="QLabel" name="label_8">
       <property name="text">
        <string>Flow Rate</string>
       </property>
      </widget>
     </item>
     <item row="1" column="1">
      <widget class="QLabel" name="label_4">
       <property name="text">
        <string>0.0</string>
       </property>
      </widget>
     </item>
     <item row="2" column="0">
      <widget class="QLabel" name="label_3">
       <property name="text">
        <string>Current</string>
       </property>
      </widget>
     </item>
     <item row="3" column="1">
      <widget class="QLabel" name="label_7">
       <property name="text">
        <string>False</string>
       </property>
      </widget>
     </item>
     <item row="2" column="1">
      <widget class="QLabel" name="label_5">
       <property name="text">
        <string>0.0</string>
       </property>
      </widget>
     </item>
     <item row="4" column="1">
      <widget class="QLabel" name="label_9">
       <property name="text">
        <string>0.0</string>
       </property>
      </widget>
     </item>
     <item row="1" column="0">
      <widget class="QLabel" name="label_2">
       <property name="text">
        <string>Voltage</string>
       </property>
      </widget>
     </item>
     <item row="3" column="0">
      <widget class="QLabel" name="label_6">
       <property name="text">
        <string>Electrodes Enabled</string>
       </property>
      </widget>
     </item>
     <item row="0" column="0">
      <widget class="QLabel" name="label">
       <property name="text">
        <string>Blue Dawn Telemetry</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>28</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuSelect_Telemetry_to_Graph">
    <property name="title">
     <string>Select Telemetry to Graph</string>
    </property>
   </widget>
   <addaction name="menuSelect_Telemetry_to_Graph"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
