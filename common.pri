equals(QT_MAJOR_VERSION, 4) {
    CONTENTACTION_DATADIR = /usr/share/contentaction
    CONTENTACTION_TESTDIR = /opt/tests/libcontentaction
    CONTENTACTION_INCLUDEDIR = /usr/include/contentaction
} else: equals(QT_MAJOR_VERSION, 5) {
    CONTENTACTION_DATADIR = /usr/share/contentaction5
    CONTENTACTION_TESTDIR = /opt/tests/libcontentaction5
    CONTENTACTION_INCLUDEDIR = /usr/include/contentaction5
}
