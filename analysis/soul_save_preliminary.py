import json,pathlib
base=pathlib.Path(r'C:\Users\warit\Desktop\agent-seacrh-virus-cut\analysis');inv=json.loads((base/'resolve_inventory.json').read_text(encoding='utf-8-sig'))
items=[]
for slug,a,b,title,hook,payoff,beat,frames,reason in [
 ('soul_003',7859,7941,'Dreadful Echo: ลุยสนามพลังจนจบเควสต์','เริ่มเข้าพื้นที่ต่อสู้ มีศัตรูและสนามพลังสีเขียวขวางทาง','รับมือฝูงศัตรู ต่อสู้ผ่านเกราะพลัง แล้วจบ Quest: Goodbye และขึ้น S+',7932,[7860,7880,7890,7920,7932,7936],'ภาพเกมมีสถานการณ์ต่อเนื่องและบทสรุปชัดเจน พร้อมเอฟเฟกต์สนามพลังและการปะทะที่ต่างจากบอสตายทันที'),
 ('soul_004',9116,9251,'ปะทะมังกรยักษ์ในสนามคริสตัล','มังกรปรากฏในสนามคริสตัลเขียวพร้อมแถบพลังบอส','ปะทะต่อเนื่องประมาณสองนาที มังกรสีขาวล้มลง ก่อนบทส่งท้ายในสนาม',9240,[9116,9122,9150,9200,9238,9240,9246,9250],'ไฟต์ยาวมีการเปลี่ยนตำแหน่ง ใช้สกิลหลายรอบ และผลแพ้ชนะที่เห็นได้ เหมาะเป็น gameplay highlight ต่างจากดันเจียนที่บอสตายในไม่กี่วินาที')]:
 c=next(c for c in inv['clips'] if 'Soul Walker - '+slug[-3:] in c['name'])
 items.append({'slug':slug,'source_clip_id':c['id'],'in_seconds':a,'out_seconds':b,'duration_seconds':b-a,'title_th':title,'category':['gameplay'],'priority':'A','hook':hook,'payoff':payoff,'beat_second':beat,'reason':reason,'transcript_evidence':[],'visual_evidence':[{'seconds':t,'description':'inspected contact sheet frame at source seconds'} for t in frames],'confidence':'high_visual_pending_transcript','notes':'Preliminary core select; exact visual source seconds established with 2-second frame samples; transcript review pending.'})
(base/'soul_selects.json').write_text(json.dumps({'sources':[c for c in inv['clips'] if 'Soul Walker - 003' in c['name'] or 'Soul Walker - 004' in c['name']],'coverage':{'visual':'all source duration at 120-second orientation; targeted gameplay windows at 10 seconds; core boundaries at 2 seconds','transcript':'pending'},'complete':False,'selects':items},ensure_ascii=False,indent=2),encoding='utf-8')
print('saved two grounded gameplay core selects')
