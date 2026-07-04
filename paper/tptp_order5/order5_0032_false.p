% order5_0032  eq1=34680 eq2=23592  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(f(Z,Z),Y)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Y),Z),f(W,f(X,Y))) )).
