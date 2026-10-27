import json
D="trump-administration"
S=dict(
 ap_mc=("AP: Maurene Comey firing ruled illegal","https://apnews.com/article/justice-department-maurene-comey-trump-be7de14f705def3bb6eeadafa7e60805"),
 mc_pdf=("Ruling (PDF), U.S. District Court, S.D.N.Y.","https://www.nysd.uscourts.gov/sites/default/files/2026-10/25cv7625%20%5B96%5D%20Opinion%2010.26.2026.pdf"),
 ap_jc=("AP: DOJ tries a third time to charge James Comey","https://apnews.com/article/comey-trump-fbi-director-prosecution-8479bdbf1bcdeeae313b453a3cd0c544"),
 cnbc_jc=("CNBC: James Comey indictment","https://www.cnbc.com/2026/10/26/james-comey-indictment-national-defense-doj-trump.html"),
 dirty=("Video: Trump on Comey (@RapidResponse47)","https://x.com/RapidResponse47/status/2114923923934441843"),
 pbs_wa=("PBS/AP: DOJ asks Washington to set aside ballots","https://www.pbs.org/newshour/politics/trump-administration-asks-washington-state-to-set-aside-ballots-from-400-voters-it-says-may-be-noncitizens"),
 ap_wa=("AP on Washington","https://apnews.com/article/washington-noncitizen-voting-63c17a3eadc9ed232fbd897afbd29b9d"),
 ap_ca=("AP on California","https://apnews.com/article/california-noncitizen-voting-justice-department-lawsuit-ed14390afb8af8fde1c2d0f6a90a0761"),
 pol_ca=("Politico: California ballots ruling","https://www.politico.com/news/2026/10/26/california-election-ballots-justice-department-ruling"),
 nbc_ak=("NBC News: DOJ lawsuit over Alaska Senate count","https://www.nbcnews.com/politics/2026-election/trump-justice-department-lawsuit-alaska-senate-rcna605229"),
 nbc_ep=("NBC News: House Democrats call for Epstein special counsel","https://www.nbcnews.com/politics/congress/house-democrats-call-doj-name-special-counsel-epstein-case-rcna605269"),
 doj_cr=("DOJ release: National Crime Victimization Survey","https://www.justice.gov/opa/pr/national-crime-victimization-survey-shows-violent-crime-plummeted-2025"),
 bjs=("BJS: Preliminary victimization estimates, NCVS 2025","https://bjs.ojp.gov/library/publications/preliminary-victimization-estimates-ncvs-2025"),
 clip_cr=("Clip: Trump on crime (@RapidResponse47)","https://x.com/RapidResponse47/status/2114862494116462675"),
 npr_snap=("NPR: SNAP chip-card rule","https://www.npr.org/2026/10/26/nx-s1-6017810/snap-benefits-ebt-card-chip-usda-rule"),
 cms=("CMS press release","https://www.cms.gov/newsroom/press-releases/cms-states-launch-275-million-initiative-recruit-retain-nurses-nursing-homes"),
 vp=("@VP on X","https://x.com/VP/status/2114899193768587646"),
 ustr=("USTR statement","https://ustr.gov/about/policy-offices/press-office/press-releases/2026/october/ambassador-greer-issues-statement-status-us-eu-detente-following-record-breaking-loan-european"),
 cnn_iran=("CNN: U.S. Iran strike plans","https://www.cnn.com/2026/10/26/politics/us-iran-strike-plans-trump"),
 cbs_iran=("CBS News live updates: Iran, oil and the Strait of Hormuz","https://www.cbsnews.com/live-updates/iran-war-trump-us-oil-gas-prices-strait-of-hormuz-midterms/"),
 nbc_ps=("NBC News: Katie Zacharia out after 5 days","https://www.nbcnews.com/politics/white-house/white-house-press-secretary-katie-zacharia-out-after-5-days-rcna603912"),
 wapo=("Washington Post: Record vacancies","https://www.washingtonpost.com/politics/2026/10/26/trump-administration-has-more-vacancies-than-any-decades/"),
 usat=("USA Today: Lawsuit over press bans","https://www.usatoday.com/story/news/nation/2026/10/26/trump-citizen-lawsuit-banning-news-outlets-white-house/92448431007/"),
 mlive=("mlive: Nicki Minaj joins Trump in Michigan","https://www.mlive.com/politics/2026/10/nicki-minaj-joins-trump-in-port-huron-urges-michigan-voters-to-back-republicans.html"),
 huff=("HuffPost: Trump on Obama","https://www.huffpost.com/entry/trump-obama-el-sayed-truth-social_n_6adde2f5e4b0320e45d2acde"),
 almon=("Al-Monitor: Libya summons U.S. envoy","https://www.al-monitor.com/originals/2026/10/libya-summons-us-envoy-protest-trump-remarks"),
 vance=("Video: Vance on Democrats (@RapidResponse47)","https://x.com/RapidResponse47/status/2114852296324731348"),
 mt=("Mississippi Today: Trump rallies for Cindy Hyde-Smith","https://mississippitoday.org/2026/10/26/trump-rallies-for-cindy-hyde-smith-in-mississippi-you-like-me/"),
 cnbc_es=("CNBC: Trump invokes 9/11 in Michigan","https://www.cnbc.com/2026/10/25/trump-invokes-911-in-urging-michigan-voters-to-oppose-el-sayed.html"),
 pol_hj=("Politico: Jeffries on Hegseth","https://www.politico.com/live-updates/2026/10/26/congress/hakeem-jeffries-pete-hegseth-impeachment-01135262"),
 europe=("Video: Trump on violence in Europe (@RapidResponse47)","https://x.com/RapidResponse47/status/2114924444670185585"),
 mediaite=("Mediaite: Hyde-Smith's nine-word speech","https://www.mediaite.com/media/news/gop-senator-lets-trump-do-all-the-talking-at-her-own-rally-after-giving-a-9-word-speech/"),
 tnd=("TND on X: El-Sayed reply","https://x.com/TND/status/2114892393648406633"),
 wh=("@WhiteHouse on X","https://x.com/WhiteHouse/status/2114839466686701604"),
 cis=("CIS: Census Bureau survey on foreign-born population","https://cis.org/Report/Census-Bureau-Survey-Shows-Total-ForeignBorn-Down-29-Million"),
 eo_list=("White House: Executive orders","https://www.whitehouse.gov/presidential-actions/executive-orders/"),
 eo_housing=("White House: Housing costs executive order","https://www.whitehouse.gov/presidential-actions/2026/10/decreasing-housing-costs-for-the-american-people/"),
 fr=("Federal Register: 2026 executive orders","https://www.federalregister.gov/presidential-documents/executive-orders/donald-trump/2026"),
)
def L(k): return f"[{S[k][0].split(':')[0] if ':' in S[k][0] else S[k][0]}]({S[k][1]})"
A=[]
def art(slug,date,title,summary,body,srcs,kps=(),status="",featured=False):
    A.append(dict(desk=D,slug=slug,date=date,title=title,summary=summary,body=body,sources=[list(S[k]) for k in srcs],key_points=list(kps),status=status,featured=featured))

art("maurene-comey-firing-ruled-illegal","2026-10-27",
 "Judge Rules Maurene Comey's Firing Was Illegal, Orders Her Reinstated With Back Pay",
 "Judge Furman ruled that Maurene Comey's firing was illegal, ordered her reinstated retroactively with back pay, and rejected DOJ's Article II argument. DOJ says it will appeal.",
 """## What happened

A federal judge ruled that Maurene Comey's firing was illegal. Judge Furman ordered her reinstated retroactively with back pay and rejected the Justice Department's Article II argument.

## What's next

DOJ says it will appeal.""",
 ["ap_mc","mc_pdf"],["Judge Furman ruled the firing illegal","Ordered reinstatement, retroactive, with back pay","Rejected DOJ's Article II argument","DOJ says it will appeal"],status="Ruling; DOJ to appeal",featured=True)

art("james-comey-charged-third-time","2026-10-26",
 "James Comey Charged a Third Time; His Lawyers Move to Dismiss",
 "A charge filed under seal on Oct. 5 and opened Monday accuses former FBI Director James Comey of passing national defense information to a reporter in 2016, plus conspiracy. His lawyers say the 10-year limit on bringing charges has run out and have moved to dismiss.",
 """**Status: Charged (alleged).** Comey has not been convicted. His lawyers have moved to dismiss.

## What happened

The Justice Department is trying a third time to charge James Comey. A charge filed under seal on October 5 and opened Monday accuses him of passing national defense information to a reporter in 2016, plus conspiracy.

## Both sides

Comey's lawyers say the 10-year limit on bringing charges has run out, and they have moved to dismiss the case.

> "Well, they're back — again." — James Comey, via CNBC

> "I think he's a dirty cop." — President Trump on Comey ([video](https://x.com/RapidResponse47/status/2114923923934441843))""",
 ["cnbc_jc","ap_jc","dirty"],["Third attempt by DOJ to charge Comey","Charge filed under seal Oct. 5, opened Monday","Accuses him of passing national defense information to a reporter in 2016, plus conspiracy","His lawyers say the 10-year limit has run out and have moved to dismiss"],status="Charged (alleged)")

art("noncitizen-ballot-fights-washington-california-alaska","2026-10-27",
 "DOJ's Ballot Fights: Washington Noncitizen Allegation, California Appeals Split, Alaska Senate Count Suit",
 "DOJ alleges that 400+ people who voted in Washington may be noncitizens — an accusation, not a finding. An appeals court split 2-1 and declined to rule on DOJ's bid to stop California from counting about 20K ballots. DOJ also sued over the Alaska Senate count.",
 """## Washington: an allegation, not a finding

**Status: Alleged (DOJ).** The Justice Department asked Washington state to set aside ballots from 400+ voters. DOJ alleges these people may be noncitizens. That is an accusation, not a finding.

## California: appeals court declines to rule

An appeals court split 2-1 and declined to rule on DOJ's bid to stop California from counting about 20,000 ballots.

*Note: An earlier AFNS briefing described this as the 9th Circuit having "tossed" DOJ's bid. The newer, more precise account is that the court split 2-1 and declined to rule.*

## Alaska: Senate count lawsuit

DOJ sued over the Alaska Senate count.""",
 ["ap_wa","pbs_wa","ap_ca","pol_ca","nbc_ak"],["Washington: DOJ alleges 400+ voters may be noncitizens (accusation, not a finding)","California: appeals court split 2-1, declined to rule on DOJ's bid over about 20K ballots","Alaska: DOJ sued over the Senate count"],status="Alleged (DOJ)")

art("house-democrats-epstein-report-special-counsel","2026-10-27",
 "House Judiciary Democrats Release Epstein Report, Call for Special Counsel; White House Responds",
 "House Judiciary Democrats released a 50-page report and called for a special counsel in the Epstein case. The White House called it \"nothing more than a desperate attempt by crazed Democrats to distract Americans.\"",
 """## What happened

House Judiciary Committee Democrats released a 50-page report and called on the Justice Department to name a special counsel in the Epstein case.

## The White House response

> "nothing more than a desperate attempt by crazed Democrats to distract Americans." — The White House""",
 ["nbc_ep"],["50-page report from House Judiciary Democrats","They call for a special counsel","White House calls it a \"desperate attempt by crazed Democrats to distract Americans\""])

art("doj-preliminary-2025-crime-data-trump-counts-fact-check","2026-10-27",
 "DOJ Preliminary Data: Serious Violent Crime Down 25% in 2025; Trump's Raw Counts Can't Be Checked Against It",
 "DOJ's preliminary 2025 numbers show serious violent crime down 25% and property crime down 19%. President Trump's raw counts, such as \"100,000 fewer rapes\" and \"700,000 fewer violent crimes,\" can't be checked against DOJ's release, which gives percentage drops in rates rather than raw counts.",
 """**Status: Preliminary data. Trump's raw counts: unverifiable against DOJ's release.**

## What the data shows

The Justice Department's preliminary 2025 numbers, from the National Crime Victimization Survey, show:

- Serious violent crime down 25%
- Property crime down 19%

These figures are preliminary.

## Checking the President's numbers

President Trump has cited raw counts such as "100,000 fewer rapes" and "700,000 fewer violent crimes" ([clip](https://x.com/RapidResponse47/status/2114862494116462675)). These can't be checked against DOJ's release, which gives percentage drops in rates rather than raw counts.

An earlier AFNS check against the Bureau of Justice Statistics' preliminary victimization estimates found the "700K fewer violent crimes" figure mostly backed by the data, but preliminary.""",
 ["doj_cr","bjs","clip_cr"],["Serious violent crime down 25% (preliminary)","Property crime down 19% (preliminary)","Trump's raw counts can't be checked against DOJ's release, which reports percentage drops in rates"],status="Preliminary; counts unverifiable")

art("usda-proposes-snap-chip-card-tap-to-pay-rule","2026-10-26",
 "USDA Proposes Chip-Enabled SNAP Cards and Tap-to-Pay at Stores",
 "USDA proposed a rule that would require chip-enabled food-assistance cards and tap-to-pay at stores.",
 """**Status: Proposed rule.**

## What happened

The U.S. Department of Agriculture proposed a rule that would require chip-enabled food-assistance (SNAP) cards and tap-to-pay at stores.""",
 ["npr_snap"],["Proposed rule, not final","Would require chip-enabled SNAP cards","Would require tap-to-pay at stores"],status="Proposed rule")

art("cms-275m-nurse-program-usda-57m-meat-poultry-processors","2026-10-26",
 "CMS Launches $275M Nursing Home Staffing Program; USDA Puts $57M Into Meat and Poultry Processors",
 "CMS launched a $275 million program that pays nurses to work at short-staffed nursing homes. Separately, USDA put $57 million into meat and poultry processors across 40 states.",
 """## CMS: $275 million for nursing home staffing

The Centers for Medicare & Medicaid Services launched a $275 million program that pays nurses to work at short-staffed nursing homes.

## USDA: $57 million for processors

USDA put $57 million into meat and poultry processors across 40 states, according to a post from the Vice President's office on X.""",
 ["cms","vp"],["CMS: $275M program pays nurses to work at short-staffed nursing homes","USDA: $57M to meat and poultry processors in 40 states"])

art("ustr-greer-warns-eu-airbus-loan-tariff-truce","2026-10-26",
 "USTR Greer Warns EU That $3.4B Airbus Loan Threatens Aircraft Tariff Truce",
 "U.S. Trade Representative Greer warned the European Union that a $3.4 billion loan to Airbus threatens the aircraft tariff truce.",
 """## What happened

U.S. Trade Representative Greer warned the European Union that a $3.4 billion loan to Airbus threatens the aircraft tariff truce between the U.S. and the EU.""",
 ["ustr"],["$3.4B loan to Airbus","USTR says it threatens the aircraft tariff truce"])

art("cnn-iran-strike-timing-hormuz-oil-claim-false","2026-10-26",
 "CNN Reports New Iran Strikes Could Launch \"Within 96 Hours\" of an Order; Trump's Hormuz Oil Claim Is False",
 "CNN reports that new strikes on Iran could launch \"within 96 hours\" of an order, likely after the midterms. Separately, President Trump's claim that more oil is moving through the Strait of Hormuz than before the war is false, per CBS News.",
 """**Status: Iran strike timing reported by CNN. Hormuz oil claim: false.**

## What CNN reported

CNN reports that new strikes on Iran could launch "within 96 hours" of an order, likely after the midterms. This is CNN's reporting; AFNS has not independently confirmed it.

## What the President said

> "do I make a deal with them, or do I finish them off?" — President Trump on Iran, via CBS News

## Fact check: oil through Hormuz

**False.** President Trump's claim that more oil is moving through the Strait of Hormuz than before the war is false, per CBS News.""",
 ["cnn_iran","cbs_iran"],["CNN reports strikes could launch \"within 96 hours\" of an order, likely after the midterms","Trump: \"do I make a deal with them, or do I finish them off?\"","Hormuz oil claim: false"],status="Reported by CNN; Hormuz claim false")

art("white-house-press-secretary-vacancy-record-vacancies","2026-10-26",
 "White House Press Secretary Job Still Empty; Administration Has Record Senate-Confirmed Vacancies",
 "The White House press secretary job is still empty since Katie Zacharia left after five days. The administration also has record vacancies in Senate-confirmed posts, per the Washington Post.",
 """## Press secretary

The White House press secretary job is still empty since Katie Zacharia left after five days in the role.

## Record vacancies

The administration has record vacancies in Senate-confirmed posts, according to the Washington Post.""",
 ["nbc_ps","wapo"],["Press secretary post empty since Katie Zacharia left after five days","Record vacancies in Senate-confirmed posts"])

art("cnn-politico-barred-air-force-one-press-ban-lawsuit","2026-10-26",
 "CNN and Politico Barred From Air Force One Again as New Lawsuit Challenges Press Bans",
 "CNN and Politico were barred from Air Force One again, and a new lawsuit challenges the press bans.",
 """## What happened

CNN and Politico were barred from Air Force One again.

## The lawsuit

A new lawsuit challenges the press bans.""",
 ["usat"],["CNN and Politico barred from Air Force One again","New lawsuit challenges the press bans"])

art("campaign-trail-mississippi-michigan-hegseth-libya","2026-10-27",
 "Campaign Trail: Trump in Mississippi and Michigan, El-Sayed Denies Claims, Jeffries on Hegseth, Libya Summons U.S. Envoy",
 "Trump rallied for Sen. Cindy Hyde-Smith in Corinth, Miss., and in Michigan with Nicki Minaj, where he stepped up attacks on Senate candidate Abdul El-Sayed. El-Sayed denies any ties to the Muslim Brotherhood; Reuters says the allegation was made without evidence. Jeffries said Democrats would hold Hegseth \"accountable.\"",
 """## Mississippi

In Corinth, President Trump campaigned for Sen. Cindy Hyde-Smith and called her Democratic opponent, Scott Colom, a "Democrat communist."

> "You like me, I like you. That's just the way it is." — Trump in Corinth

> "We did a rally in the north or the south, I don't know where the hell it was." — Trump on his 2019 Mississippi rally

Hyde-Smith gave a nine-word speech at her own rally:

> "Is this not the best president in our lifetime?" — Sen. Cindy Hyde-Smith ([Mediaite](https://www.mediaite.com/media/news/gop-senator-lets-trump-do-all-the-talking-at-her-own-rally-after-giving-a-9-word-speech/))

**Next stops:** Texas today, Ohio Wednesday, Florida Friday and Iowa Sunday.

## Michigan

Trump held a rally in Michigan with Nicki Minaj ([mlive](https://www.mlive.com/politics/2026/10/nicki-minaj-joins-trump-in-port-huron-urges-michigan-voters-to-back-republicans.html)). He stepped up his attacks on Senate candidate Abdul El-Sayed and invoked 9/11.

> "I'm here to keep a jihadist, Muslim Brotherhood member from becoming a United States senator." — Trump on El-Sayed

**Status of the Muslim Brotherhood claim: made without evidence, and denied.** Reuters says Mike Rogers made the allegation "without evidence." El-Sayed denies any ties to the Muslim Brotherhood.

> "I'll be Senator Mohammed to you, bro." — Abdul El-Sayed ([TND](https://x.com/TND/status/2114892393648406633))

Trump also called former President Obama "a grossly incompetent President" ([HuffPost](https://www.huffpost.com/entry/trump-obama-el-sayed-truth-social_n_6adde2f5e4b0320e45d2acde)).

## Hegseth and House Democrats

House Democratic Leader Hakeem Jeffries said Democrats would hold Defense Secretary Pete Hegseth "accountable" if they win the House. That edges toward impeachment without committing to it.

Vice President Vance, about Democrats: "a fat load of BULLSHIT." ([video](https://x.com/RapidResponse47/status/2114852296324731348))

## Libya

Libya summoned the U.S. envoy over his "shithouse countries" remark ([Al-Monitor](https://www.al-monitor.com/originals/2026/10/libya-summons-us-envoy-protest-trump-remarks)).

## Also said

> "I don't worry about that at all. That's an immigration problem." — Trump on violence in Europe ([video](https://x.com/RapidResponse47/status/2114924444670185585))""",
 ["mt","mediaite","mlive","cnbc_es","tnd","huff","pol_hj","vance","almon","europe"],
 ["Trump rallied for Hyde-Smith in Corinth, called opponent Scott Colom a \"Democrat communist\"","El-Sayed denies Muslim Brotherhood ties; Reuters says the allegation was made \"without evidence\"","Jeffries: Democrats would hold Hegseth \"accountable\" if they win the House","Libya summoned the U.S. envoy over his \"shithouse countries\" remark","Next stops: Texas, Ohio, Florida, Iowa"],
 status="El-Sayed claim: without evidence, denied")

art("fact-check-hormuz-immigration-crime-el-sayed-washington-ballots","2026-10-27",
 "Fact Check: Hormuz Oil, \"7 Million Fewer Illegal Immigrants,\" Crime Counts, El-Sayed and Washington Ballots",
 "A roundup of claims checked this week: the Hormuz oil claim and the viral \"7 million fewer illegal immigrants\" figure are false; Trump's raw crime counts can't be checked against DOJ's release; the El-Sayed Muslim Brotherhood claim was made without evidence, per Reuters, and is denied; Washington's \"400 noncitizen voters\" is still only DOJ's allegation.",
 """**Status: Fact check.**

## More oil through Hormuz than before the war — FALSE

President Trump's claim that more oil is moving through the Strait of Hormuz than before the war is false, per CBS News. [More](../cnn-iran-strike-timing-hormuz-oil-claim-false/)

## "7 million fewer illegal immigrants" — FALSE

The viral "7 million fewer illegal immigrants" figure is false. The White House's 2.3 million number is a preliminary net estimate.

## "100,000 fewer rapes" and "700,000 fewer violent crimes" — UNVERIFIABLE against DOJ's release

These raw counts can't be checked against DOJ's release, which gives percentage drops in rates rather than raw counts. DOJ's own data is preliminary. [More](../doj-preliminary-2025-crime-data-trump-counts-fact-check/)

## El-Sayed and the Muslim Brotherhood — MADE WITHOUT EVIDENCE, DENIED

Reuters says Mike Rogers made the allegation "without evidence," and El-Sayed denies it. [More](../campaign-trail-mississippi-michigan-hegseth-libya/)

## "400 noncitizen voters" in Washington — ALLEGATION

This is still only DOJ's allegation, not a finding. [More](../noncitizen-ballot-fights-washington-california-alaska/)""",
 ["cbs_iran","cis","doj_cr","clip_cr","cnbc_es","ap_wa"],
 ["Hormuz oil claim: false","\"7 million fewer illegal immigrants\": false; the White House's 2.3M is a preliminary net estimate","Trump's raw crime counts: unverifiable against DOJ's release","El-Sayed claim: made without evidence (Reuters), denied","Washington 400 noncitizen voters: DOJ allegation"],status="Fact check")

# daily roundup
items=[a for a in A]
def link(slug,t): return f"[{t}](../{slug}/)"
body="""The AFNS daily briefing on the Trump administration for Tuesday, October 27, 2026. Each item links to the full AFNS article and its sources.

## Courts and DOJ

- """+link("maurene-comey-firing-ruled-illegal","Judge rules Maurene Comey's firing illegal")+""": ordered reinstated retroactively with back pay; DOJ says it will appeal.
- """+link("james-comey-charged-third-time","James Comey charged a third time")+""" (charged, alleged): his lawyers say the 10-year limit has run out and have moved to dismiss.
- """+link("noncitizen-ballot-fights-washington-california-alaska","Ballot fights")+""": DOJ's Washington noncitizen claim is an allegation; an appeals court split 2-1 and declined to rule on California; DOJ sued over the Alaska Senate count.
- """+link("house-democrats-epstein-report-special-counsel","Epstein report")+""": House Judiciary Democrats call for a special counsel; the White House calls it a "desperate attempt."

## Policy

- """+link("doj-preliminary-2025-crime-data-trump-counts-fact-check","Crime data")+""": preliminary numbers show serious violent crime down 25%, property crime down 19%.
- """+link("usda-proposes-snap-chip-card-tap-to-pay-rule","SNAP cards")+""": USDA proposes chip-enabled cards and tap-to-pay.
- """+link("cms-275m-nurse-program-usda-57m-meat-poultry-processors","CMS and USDA funding")+""": $275M nursing home staffing program; $57M for meat and poultry processors.
- """+link("ustr-greer-warns-eu-airbus-loan-tariff-truce","Trade")+""": USTR warns the EU over a $3.4B Airbus loan.
- """+link("cnn-iran-strike-timing-hormuz-oil-claim-false","Iran")+""": CNN reports strikes could launch "within 96 hours" of an order.
- **Executive orders:** No new executive orders were reported. Recent orders include housing costs and wind-turbine imports (Oct. 22) and EO 14437 on women's health (Oct. 19). [White House list](https://www.whitehouse.gov/presidential-actions/executive-orders/) · [Housing EO](https://www.whitehouse.gov/presidential-actions/2026/10/decreasing-housing-costs-for-the-american-people/) · [Federal Register](https://www.federalregister.gov/presidential-documents/executive-orders/donald-trump/2026)

## Personnel and press

- """+link("white-house-press-secretary-vacancy-record-vacancies","Press secretary job still empty; record vacancies")+""".
- """+link("cnn-politico-barred-air-force-one-press-ban-lawsuit","CNN and Politico barred from Air Force One again")+"""; a new lawsuit challenges the bans.

## Campaign trail

- """+link("campaign-trail-mississippi-michigan-hegseth-libya","Mississippi, Michigan, Hegseth, Libya")+""": rallies, El-Sayed's denial, Jeffries on Hegseth, and Libya summoning the U.S. envoy.
- Top administration post of the day: the White House's "Dems are washed up. 🎷" at about 2.6M views ([X](https://x.com/WhiteHouse/status/2114839466686701604)).

## Fact checks

- """+link("fact-check-hormuz-immigration-crime-el-sayed-washington-ballots","This week's fact checks")+""": Hormuz oil claim false; "7 million fewer illegal immigrants" false; Trump's crime counts unverifiable against DOJ's release.

*The AFNS daily Trump administration briefing posts every morning.*"""
allsrc=[]
for a in A:
    for s in a["sources"]:
        if s not in allsrc: allsrc.append(s)
for k in ["eo_list","eo_housing","fr","wh"]:
    if list(S[k]) not in allsrc: allsrc.append(list(S[k]))
A.append(dict(desk=D,slug="daily-trump-administration-briefing-2026-10-27",date="2026-10-27",
 title="Daily Trump Administration Briefing — Oct. 27, 2026",
 summary="Maurene Comey's firing ruled illegal, James Comey charged a third time, DOJ ballot fights in Washington, California and Alaska, preliminary crime data, a SNAP card rule, campaign trail moments and this week's fact checks.",
 body=body,sources=allsrc,key_points=["Maurene Comey firing ruled illegal; DOJ to appeal","James Comey charged a third time (alleged)","Washington noncitizen claim is a DOJ allegation","Crime data is preliminary","Hormuz and \"7 million\" claims are false"],status="Daily briefing"))
json.dump(A,open("/workspace/afns-research/batch2.json","w"),indent=1,ensure_ascii=False)
print(len(A))
# coverage check: every URL in the research file appears
import re
src=open("/workspace/afns-research/trump-admin-2026-10-27.txt").read()
urls=set(re.findall(r"\((https?://[^)\s]+)\)",src))
used=json.dumps(A,ensure_ascii=False)
print("unused urls:",[u for u in urls if u not in used])
