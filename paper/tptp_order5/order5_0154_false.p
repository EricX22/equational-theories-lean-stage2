% order5_0154  eq1=43283 eq2=52835  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X] : ( f(X,X) = f(X,f(f(X,X),f(X,X))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(f(f(Z,f(W,Y)),U),X) )).
