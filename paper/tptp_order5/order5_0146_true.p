% order5_0146  eq1=30183 eq2=40231  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(Y,f(f(X,X),Y))),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Y,Z)),Y),Z),W) )).
