% hard3_0268  eq1=2525 eq2=3820  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(X,Z),W)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,Z),f(X,Y)) )).
