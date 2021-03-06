# SRE's review of Democracy

### Day One

We've been handed this old legacy system called "Democracy". It's an emergency. Old maintainers are saying it's misbehaving lately but they have no idea how to fix it. We've had a meeting with them to find out as much as possible about the system but it turns out that all the original team members have left the company long time ago and that the current team doesn't have much understanding of the system beyond some basic operational knowledge.

We've done some cursory code review, focusing not so much on business logic but rather on the stuff that could possibly help us to tame it: Monitoring, reliability characteristics, feedback loops, automation already in place. First impression: Oh, God, is the thing complex! Second impression: The system is vaguely modular. However, each module is strongly coupled with every other module. It's organically grown legacy system at its worst.

That being said, we've found a hint why the system may have worked OK for so long. There's this redundancy system called "Separation of Powers". It reminds me of the Tandem computers from 70's.

### Day Two

We were wrong. "Separation of Powers" is not a system for redundancy. Each part of the system ("branch") has different business logic, however, each also acts as a watchdog process for the other branches. When it detects misbehavior it tries to apply corrective measures using its own business logic. Gasp!

Things are not looking good. Still searching for monitoring.

### Day Three

Hooray! We've found the monitoring! It turns out that "Election" is done once per four years. Each component reports its health (1 bit) to the central location. The data flow is so low that we have overlooked it until now. We are thinking of shortening the reporting period but the subsystem is so deeply coupled with other subsystems that doing so may easily lead to cascading failure.

In other news, there seems to be some redundancy after all. We've found a full-blown backup control system ("Shadow Cabinet") that is inactive at the moment but may be able to take over if there's a major failure. Investigating.

### Day Four

Today we've found yet another monitoring system. It's called "FreePress". As the name suggests it was open-sourced some time ago, but the corporate version have evolved quite a bit since then, so the docs are not really helpful. The bad news is that it's badly intertwined with the production systems. The metrics look more or less OK as long as everything is working smoothly. It's not clear though what the behavior will be if things go south. It may distort the metrics or even fail entirely, leaving us with no data whatsoever at the moment of crisis.

By the way, the "Election" thing may not be monitoring after all. My suspicion is that it's actually a feedback loop triggering some corrective measures in case of problem.

### Day Five

The most important metric seems to be this big graph labeled "GDP". As far as we understand it, it's supposed to indicate overall health of the system, but drilling into the code suggests that it's actually a throughput metric. If throughput goes down there's certainly a problem. However, it's not clear why increasing throughput should be considered primary health factor.

More news on the "Election" subsystem. We found a floppy disk with the design doc and it turns out that it's not a feedback loop after all. It's a distributed consensus algorithm (think Paxos). The historical context is that they've used to run several control systems in parallel (for redundancy reasons, maybe?) which resulted in lots of race conditions and outages. "Election" was put in place to ensure that only one control system acts as a master at any point of time. The consensus algorithm is based on PTP (Peaceful Transfer of Power) protocol. The gist is that when most components are reporting unhealthiness it is treated as a failure of the control system and a backup ("Shadow Cabinet") is automatically activated. Main control system becomes the backup. It's not clear how is it supposed to be fixed while in backup mode though.

### Day Six

I met guys from Theocracy Inc. in a bar last night and complained about the GDP metric. They've suggested using GNH ("Gross National Happiness") metric instead. We should definitely add such console.

We've also dug into the operational practices for "Democracy". It turns out there was no postmortem culture. Outages were followed by covering up and blame-shifting. The most damaging consequence is that we have no clear understanding of the failure modes of the system.

We now have more understanding of one the "Separation of Powers" branches, the "Judiciary" branch. It evaluates whether components are behaving according to pre-defined set of rules. If they are not, they are removed from production and put into suspended state ("Jail"). It's not clear how are they supposed to be fixed while suspended. (We've seen a similar problem with the backup control system so we may be missing something essential here.)

It's Sunday tomorrow. I am taking a day off to think about how to solve the mess. Hopefully, nothing will blow up while I am away.

**Feb 7th, 2017**