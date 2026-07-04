% order5v2_1159  eq1=12186 eq2=10852  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),Z),f(W,Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(X,f(Y,X)),f(Y,X))) )).
