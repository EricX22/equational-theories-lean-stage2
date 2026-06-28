% hard3_0326  eq1=3039 eq2=3065  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),W),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(f(X,Y),X),X),X) )).
