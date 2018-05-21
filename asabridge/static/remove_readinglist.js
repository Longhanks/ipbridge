ObjC.import('Foundation')
ObjC.import('CoreGraphics')

args = $.NSProcessInfo.processInfo.arguments
argv = []
for (i = 0; i < args.count; i++) {
    argv.push(ObjC.unwrap(args.objectAtIndex(i)))
}
delete args

readingListItemIndex = parseInt(argv[4])

Safari = Application("Safari")
SE = Application('System Events')
SF = SE.processes.byName('Safari')

if (!Safari.running()) {
    Safari.activate()
    delay(2)
} else {
    Safari.documents.push(Safari.Document())
}

SF.frontmost = true

window = SF.windows[0]
splitterGroup = window.splitterGroups[0]
if (splitterGroup.groups.length === 0) {
    menuView = SF.menuBars[0].menuBarItems[4]
    menuView.click()
    toggleSideBarButton = menuView.menus[0].menuItems[7]
    toggleSideBarButton.click()
}

readingListButton = splitterGroup.groups[0].radioGroups[0].radioButtons[1]
readingListButton.click()

readingList = SF.windows[0].splitterGroups[0].groups[0].scrollAreas[0].tables[0]
realItems = []
for (i = 0; i < readingList.rows.length; ++i) {
    if (readingList.rows[i].uiElements[0].groups.length !== 0) {
        realItems.push(readingList.rows[i].uiElements[0])
    }
}

x = realItems[readingListItemIndex].position()[0] + 5
y = realItems[readingListItemIndex].position()[1] + 5

rightDown = $.CGEventCreateMouseEvent($(), $.kCGEventRightMouseDown, $.CGPointMake(x, y), $.kCGMouseButtonRight)
$.CGEventPost($.kCGHIDEventTap, rightDown)
$.CFRelease(rightDown)

delay(0.015)

rightUp = $.CGEventCreateMouseEvent($(), $.kCGEventRightMouseUp, $.CGPointMake(x, y), $.kCGMouseButtonRight);
$.CGEventPost($.kCGHIDEventTap, rightUp)
$.CFRelease(rightUp)

readingList.menus[0].menuItems[5].actions.byName("AXPress").perform()

Safari.windows[0].close()

