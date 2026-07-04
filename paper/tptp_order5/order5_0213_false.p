% order5_0213  eq1=1422 eq2=22163  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),U),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Z,W)),f(Z,f(W,Z))) )).
