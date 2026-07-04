% order5_0036  eq1=56149 eq2=11444  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,X),f(Y,Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(Y,Y)),f(Z,W))) )).
