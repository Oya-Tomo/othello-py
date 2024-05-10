class ProgressManager:
    def __init__(
        self,
        batch: int,
        train_data_count: int,
        test_data_count: int,
    ) -> None:
        self.epoch = 0
        self.batch = batch
        self.train_data_count = train_data_count
        self.test_data_count = test_data_count

        self._train_progress = 0
        self._train_loss = 0
        self._train_correct = 0
        self._train_count = 0

        self._test_progress = 0
        self._test_loss = 0
        self._test_correct = 0
        self._test_count = 0

    def epoch_start(self, epoch: int):
        self.epoch = epoch
        print(f"epoch {epoch} start")

    def count_up_train_progress(self):
        self._train_progress += 1
        print(f"\rprogress : {self._train_progress}/{self.train_data_count} ", end="")

    def count_up_test_progress(self):
        self._test_progress += 1
        print(f"\rprogress : {self._test_progress}/{self.test_data_count} ", end="")

    def finish_progress(self):
        print("> finished")

    def count_train_correct(self, correct, count):
        self._train_correct += correct
        self._train_count += count

    def count_test_correct(self, correct, count):
        self._test_correct += correct
        self._test_count += count

    def sum_train_loss(self, loss):
        self._train_loss += loss

    def sum_test_loss(self, loss):
        self._test_loss += loss

    def reset(self):
        self._train_correct = 0
        self._train_loss = 0
        self._train_progress = 0
        self._train_count = 0

        self._test_correct = 0
        self._test_loss = 0
        self._test_progress = 0
        self._test_count = 0

    def show_train_loss_accuracy(self):
        print(
            f"train eval result > loss : {self._train_loss * self.batch / self._train_count}, accuracy : {self._train_correct / self._train_count}"
        )

    def show_test_loss_accuracy(self):
        print(
            f"test  eval result > loss : {self._test_loss * self.batch / self._test_count}, accuracy : {self._test_correct / self._test_count}"
        )
