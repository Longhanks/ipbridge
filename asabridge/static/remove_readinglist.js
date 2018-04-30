ObjC.import('Foundation')

var args = $.NSProcessInfo.processInfo.arguments
var argv = []
for (var i = 0; i < args.count; i++) {
    argv.push(ObjC.unwrap(args.objectAtIndex(i)))
}
delete args

var readingListItemIndex = parseInt(argv[4])

var Safari = Application("Safari")
var SE = Application('System Events')
var SF = SE.processes.byName('Safari')

if (!Safari.running()) {
    Safari.activate()
    delay(2)
} else {
    Safari.documents.push(Safari.Document())
}

SF.frontmost = true

var window = SF.windows[0]
var splitterGroup = window.splitterGroups[0]
if (splitterGroup.groups.length === 0) {
    var menuBar = SF.menuBars[0]
    var menuView = menuBar.menuBarItems[4]
    menuView.click()
    var toggleSideBarButton = menuView.menus[0].menuItems[7]
    toggleSideBarButton.click()
}

var readingListButton = splitterGroup.groups[0].radioGroups[0].radioButtons[1]
readingListButton.click()

var splitterGroup = SF.windows[0].splitterGroups[0]
var sideBar = splitterGroup[0]
var readingList = splitterGroup.groups[0].scrollAreas[0].tables[0]
var realItems = []
for (var i = 0; i < readingList.rows.length; ++i) {
    if (readingList.rows[i].uiElements[0].groups.length != 0) {
        realItems.push(readingList.rows[i].uiElements[0])
    }
}

var x = realItems[readingListItemIndex].position()[0] + 5
var y = realItems[readingListItemIndex].position()[1] + 5

var app = Application.currentApplication()
app.includeStandardAdditions = true
app.doShellScript(`/usr/local/bin/cliclick rc:${x},${y}`)
readingList.menus[0].menuItems[5].actions.byName("AXPress").perform()

Safari.windows[0].close()

