% order5_0232  eq1=49822 eq2=15796  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Y,f(Y,f(X,Z))),W) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(f(f(Z,f(X,W)),U),Y)) )).
