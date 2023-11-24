This should work without any changes if you try deploying it directly on Railway.

 I will also note, I chose to use OpenAI liberally, and often chose extroardinarily expensive solutions. As an example, I use RAG (thanks for the idea Gabe) to find the most pieces of the transcript to the question. Given the transcript looks a bit ugly, I have OpenAI summarize the source of truth that it uses to answer the question and show that to the user.

TODO: 
I know the solution is imperfect. If I were to invest some more effort, here are changes I would make:
1. The summary will not work for infinite-length videos. 
2. Transcript may break.
3. My choice for chunking is poor.
4. Timestamps are for the beginning of the chunk

TODO: 
1. save transcript in accessible format. probably need to connect a db and store transcript / summary
2. reduce latency?
