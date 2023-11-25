This should work without any changes if you try deploying it directly on Railway.

I will also note, I used OpenAI liberally, and often chose extroardinarily expensive solutions that improve end user UX. As an example, when a user submits a question, I search for the most similar pieces of the transcript and prefeed that into the model. I want to show users the ~approximate timestamp so they can look at the source of truth for that data, but the YT API returns the transcript in a pretty ugly format, so I use OpenAI to summarize that source-of-truth. 

I know this solution is imperfect. If I were to invest some more effort, here are changes I would make:
1. The summary will not work for videos of infinite length (beyond OpenAI's max context window). If I wanted to fix this, I could split the transcript into chunks of max-context-length, summarize those, and then ask the LLM to combine my summaries! 
2. I chose a pretty poor strategy for chunking (split by sentence, added together until it crosses 500 tokens). I didn't have a great strategy to do this, but it would be much more effective to split by topic. As a result, the timestamp often will not take you to the part relevant to the question.

TODO: 
1. Clean up the code
2. Save transcript in an accessible format? Probably need to connect a DB and store the transcript / summary.
3. Reduce latency?
