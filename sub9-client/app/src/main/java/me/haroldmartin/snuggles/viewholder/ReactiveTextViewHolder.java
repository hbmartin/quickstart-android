package me.haroldmartin.snuggles.viewholder;

import android.view.View;
import android.widget.TextView;

public class ReactiveTextViewHolder<T> extends ReactiveRecylerAdapter.ReactiveViewHolder<T> {

    private TextView label;
    private T currentItem;

    public ReactiveTextViewHolder(View itemView) {
        super(itemView);
        label = (TextView) itemView.findViewById(android.R.id.text1);
    }

    @Override
    public void setCurrentItem(T currentItem) {
        this.currentItem = currentItem;
        this.label.setText(currentItem.toString());
    }

    public T getCurrentItem() {
        return currentItem;
    }
}
