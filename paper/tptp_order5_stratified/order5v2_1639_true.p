% order5v2_1639  eq1=33042 eq2=57257  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(f(X,Z),X),Y)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,f(W,Y)),X) )).
