% order5v2_0331  eq1=37838 eq2=42886  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,f(Z,Z))),X),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Y,f(Z,f(f(W,X),Y))) )).
