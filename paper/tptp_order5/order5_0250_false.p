% order5_0250  eq1=31520 eq2=940  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(f(Z,X),f(X,Z))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Y,Z),f(W,Z))) )).
