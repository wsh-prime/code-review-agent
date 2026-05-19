
    def fassistant(self, msg):
        return {"role": "assistant", "content": msg}

    def next(self, messages: List[Dict[str, str]], prompt=None, *, step_name=None):
        if prompt:
            messages += [{"role": "user", "content": prompt}]

        logger.debug(f"Creating a new chat completion: {messages}")
        response = openai.ChatCompletion.create(
            messages=messages,
            stream=True,
            model=self.model,
            temperature=self.temperature,
        )

        chat = []
        for chunk in response:
            delta = chunk["choices"][0]["delta"]  # type: ignore
            msg = delta.get("content", "")
            print(msg, end="")
            chat.append(msg)
        print()
        messages += [{"role": "assistant", "content": "".join(chat)}]
        logger.debug(f"Chat completion finished: {messages}")

        self.update_token_usage_log(
            messages=messages, answer="".join(chat), step_name=step_name
        )

        return messages

    def update_token_usage_log(self, messages, answer, step_name):
        prompt_tokens = self.num_tokens_from_messages(messages)
        completion_tokens = self.num_tokens(answer)
        total_tokens = prompt_tokens + completion_tokens

        self.cumulative_prompt_tokens += prompt_tokens
        self.cumulative_completion_tokens += completion_tokens
        self.cumulative_total_tokens += total_tokens

        self.token_usage_log.append(
            TokenUsage(
                step_name=step_name,
                in_step_prompt_tokens=prompt_tokens,
                in_step_completion_tokens=completion_tokens,
                in_step_total_tokens=total_tokens,
                total_prompt_tokens=self.cumulative_prompt_tokens,
                total_completion_tokens=self.cumulative_completion_tokens,
                total_tokens=self.cumulative_total_tokens,
            )