# Executed through Resolve's sandbox after SELECTS and INVENTORY are injected.
# No filesystem, network, source modifications, render or destructive timeline calls.
assert project.GetName() == 'KT404_2026-09-29', 'Unexpected active Resolve project'
mp=project.GetMediaPool()
root=mp.GetRootFolder()
def get_clips(folder):
    found={c.GetMediaId():c for c in folder.GetClipList()}
    for f in folder.GetSubFolderList(): found.update(get_clips(f))
    return found
clips=get_clips(root)
meta={c['id']:c for c in INVENTORY}
existing={project.GetTimelineByIndex(i).GetName():project.GetTimelineByIndex(i) for i in range(1,project.GetTimelineCount()+1)}
parent=next((f for f in root.GetSubFolderList() if f.GetName()=='Shorts_2026-09-29'),None)
if parent is None: parent=mp.AddSubFolder(root,'Shorts_2026-09-29')
bins={}
for name in ['Gameplay','Fun','Meme']:
    bins[name]=next((f for f in parent.GetSubFolderList() if f.GetName()==name),None) or mp.AddSubFolder(parent,name)
results=[]
for s in SELECTS:
    name=s['timeline_name']; cid=s['source_clip_id']; c=clips[cid]; fps=float(meta[cid]['fps'])
    start=round(s['in_seconds']*fps); stop=round(s['out_seconds']*fps)
    assert 0<=start<stop<=int(meta[cid]['frames']), 'Invalid source range'
    assert 30<=(stop-start)/fps<=180, 'Duration outside requested range'
    if name in existing:
        results.append({'name':name,'status':'existing_skipped'})
        continue
    assert mp.SetCurrentFolder(bins.get(s['category'].title(),bins['Gameplay']))
    tl=mp.CreateEmptyTimeline(name)
    assert tl is not None, 'Timeline creation failed'
    assert project.SetCurrentTimeline(tl)
    settings_ok=tl.SetSettings({'useCustomSettings':'1','timelineFrameRate':str(int(fps)),'timelineResolutionWidth':'1920','timelineResolutionHeight':'1080'})
    actual_fps=float(tl.GetSettings()['timelineFrameRate'])
    assert actual_fps==fps, 'Custom timeline frame rate did not apply'
    tc_ok=tl.SetStartTimecode('01:00:00:00')
    record=tl.GetStartFrame()
    added=mp.AppendToTimeline([{'mediaPoolItem':c,'startFrame':start,'endFrame':stop,'recordFrame':record}])
    assert added, 'Source append failed'
    video=tl.GetItemListInTrack('video',1)
    audio=tl.GetItemListInTrack('audio',1)
    assert len(video)==1 and len(audio)>=1, 'Missing video or audio'
    linked=tl.SetClipsLinked(video+audio,True)
    notes='Source: '+s['slug']+' '+str(s['in_seconds'])+'-'+str(s['out_seconds'])+' sec\n'+s.get('reason','')+'\nHook: '+s.get('hook','')+'\nPayoff: '+s.get('payoff','')
    color={'gameplay':'Blue','fun':'Green','meme':'Yellow'}.get(s['category'],'Blue')
    marker_ok=tl.AddMarker(0,color,s['title_th'],notes,stop-start,'katy404_short_'+s['select_id'])
    beat=s.get('beat_second')
    if beat is not None and s['in_seconds']<beat<s['out_seconds']:
        tl.AddMarker(round((beat-s['in_seconds'])*fps),'Red','Payoff',s.get('payoff',''),1,'katy404_payoff_'+s['select_id'])
    tl.SetTrackName('video',1,'Gameplay + original framing')
    tl.SetTrackName('audio',1,'Original stream audio')
    def describe(it):
        return {'name':it.GetName(),'start':it.GetStart(),'end':it.GetEnd(),'duration':it.GetDuration(),'source_start':it.GetSourceStartFrame(),'source_end':it.GetSourceEndFrame(),'source_id':it.GetMediaPoolItem().GetMediaId(),'linked_count':len(it.GetLinkedItems())}
    v=[describe(x) for x in video]; a=[describe(x) for x in audio]
    good=all(x['start']==record and x['end']==record+stop-start and x['duration']==stop-start and x['source_id']==cid for x in v+a)
    good=good and v[0]['source_start']==start and v[0]['source_end']==stop
    assert good, 'Timeline source/duration verification failed'
    results.append({'name':name,'select_id':s['select_id'],'status':'created_verified','id':tl.GetUniqueId(),'fps':actual_fps,'resolution':'1920x1080','duration_seconds':(tl.GetEndFrame()-record)/fps,'start_timecode':tl.GetStartTimecode(),'video':v,'audio':a,'linked':linked,'marker':marker_ok,'settings':settings_ok,'source_in_frame':start,'source_out_frame_exclusive':stop})
mp.SetCurrentFolder(parent)
saved=resolve.GetProjectManager().SaveProject()
result={'project':project.GetName(),'saved':saved,'results':results,'timeline_count':project.GetTimelineCount()}
