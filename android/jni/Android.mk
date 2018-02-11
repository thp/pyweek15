LOCAL_PATH := $(call my-dir)

PYTHON_VERSION_MINOR := 3.6
PYTHON_VERSION_PATCH := 4

PYTHON_VERSION := $(PYTHON_VERSION_MINOR).$(PYTHON_VERSION_PATCH)

include $(CLEAR_VARS)
LOCAL_MODULE := python$(PYTHON_VERSION_MINOR)
LOCAL_SRC_FILES := libpython$(PYTHON_VERSION_MINOR)m.a
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := libonewhaletrip
LOCAL_SRC_FILES := main.c
LOCAL_CFLAGS := -fvisibility=hidden -I. -I../../core/ -I../Python-$(PYTHON_VERSION)/Include/ -I../Python-$(PYTHON_VERSION)/
LOCAL_LDFLAGS := -fvisibility=hidden -fno-rtti -fno-exceptions -lGLESv2 -lz -landroid
LOCAL_STATIC_LIBRARIES := python$(PYTHON_VERSION_MINOR)
LOCAL_CPPFLAGS += -ffunction-sections -fdata-sections
LOCAL_CFLAGS += -ffunction-sections -fdata-sections
LOCAL_LDFLAGS += -Wl,--gc-sections
include $(BUILD_SHARED_LIBRARY)

