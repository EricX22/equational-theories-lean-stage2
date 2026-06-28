% hard3_0261  eq1=2483 eq2=1461  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),Y)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(Z,f(X,X))) )).
