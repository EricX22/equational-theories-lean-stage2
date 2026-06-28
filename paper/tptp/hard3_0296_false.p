% hard3_0296  eq1=2816 eq2=3197  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(Z,W)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(Y,Z),Y),Y),X) )).
