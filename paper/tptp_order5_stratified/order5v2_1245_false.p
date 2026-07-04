% order5v2_1245  eq1=30943 eq2=12102  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(f(W,W),X))),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(f(Y,Y),X),f(X,X))) )).
