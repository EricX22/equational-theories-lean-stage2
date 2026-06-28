% hard3_0283  eq1=2678 eq2=2039  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,X),X),f(Y,Z)) )).
